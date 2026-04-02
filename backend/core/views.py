from django.contrib.auth import authenticate, login, logout
from .models import User, Progress, QuizAttempt, Badge, Certificate, Recommendation, ChatMessage, Module, Lesson, UserProgress, Challenge, Quiz, Question, UserMastery, DiagnosticAttempt, DiagnosticQuestionMeta
from rest_framework import generics, permissions, viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, ProgressSerializer, QuizAttemptSerializer, BadgeSerializer, CertificateSerializer, RecommendationSerializer, ChatMessageSerializer, ModuleSerializer, LessonSerializer, UserProgressSerializer, QuizSerializer, QuestionSerializer, ChallengeSerializer, UserMasterySerializer, DiagnosticAttemptSerializer, DiagnosticQuestionMetaSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from assessments.services import log_assessment_interaction
from lessons.models import LessonProfile
from users.services import update_engagement
from gamification.services import add_xp, update_streak, award_badge
from evaluation.services import log_recommendation_event, mark_recommendation_accepted, mark_recommendation_completed, get_or_assign_strategy
from recommendation.services import update_topic_velocity, update_shift_outcome, get_behavior, compute_difficulty_adjustment, log_difficulty_shift
from analytics.services.skill_analysis import analyze_user_skill_gaps
from core.services.ai_quiz_generator import generate_quiz_from_lesson
import subprocess
import os
import uuid
import sys
import tempfile
import json
import re
import logging
import os
import urllib.request as urlreq
import urllib.error as urlerr

logger = logging.getLogger(__name__)

def normalize_level_for_score(score):
    # Ensure score is normalized to 0-100 scale
    s = float(score)
    if s < 50:
        return "Beginner"
    if s < 80:
        return "Intermediate"
    return "Pro"

def map_level_to_db(level):
    if not level:
        return "Beginner"
    lower = level.strip().lower()
    if lower in ["pro", "advanced"]:
        return "Pro"  # Database stores as "Pro"
    if lower == "intermediate":
        return "Intermediate"
    return "Beginner"

def update_user_mastery(user, module_id, score, source, topic=None):
    normalized_score = float(score)
    if normalized_score > 1:
        normalized_score = normalized_score / 100
    normalized_score = max(0.0, min(1.0, normalized_score))
    existing = UserMastery.objects.filter(user=user, module_id=module_id).first()
    if existing:
        new_score = round(existing.mastery_score * 0.7 + normalized_score * 0.3, 4)
        existing.mastery_score = new_score
        existing.last_source = source
        existing.save(update_fields=["mastery_score", "last_source", "last_updated"])
    else:
        new_score = round(normalized_score, 4)
        UserMastery.objects.create(
            user=user,
            module_id=module_id,
            mastery_score=new_score,
            last_source=source,
        )
    mastery_vector = user.mastery_vector or {}
    module_difficulty_map = mastery_vector.get("_module_difficulty", {})
    
    difficulty_label = normalize_level_for_score(new_score * 100)

    if topic:
        mastery_vector[topic] = new_score
    else:
        module_key = str(module_id)
        mastery_vector[module_key] = new_score
        # Also update _module_difficulty map for consistency across adaptive systems
        module_difficulty_map[module_key] = difficulty_label
        module_difficulty_map[module_key.replace("-", "_")] = difficulty_label
        
    mastery_vector["_module_difficulty"] = module_difficulty_map
    user.mastery_vector = mastery_vector
    user.save(update_fields=["mastery_vector"])
    if topic:
        update_topic_velocity(user, topic, new_score)
    return new_score

def is_level_completed(user, module_id, db_level):
    lesson_ids = list(Lesson.objects.filter(module_id=module_id, difficulty=db_level).values_list("id", flat=True))
    if not lesson_ids:
        return False
    user_id = user.original_uuid or str(user.id)
    completed_count = UserProgress.objects.filter(
        user_id=user_id,
        lesson_id__in=lesson_ids,
        completed=True,
    ).count()
    return completed_count == len(lesson_ids)

def _progress_user_id(user):
    return user.original_uuid or str(user.id)

def _quiz_completed(user):
    try:
        from assessments.models import DiagnosticQuizAttempt
        has_completed_attempt = DiagnosticQuizAttempt.objects.filter(user=user, status="COMPLETED").exists()
        if has_completed_attempt:
            return True
    except Exception:
        pass
    return bool(getattr(user, "has_taken_quiz", False) or getattr(user, "diagnostic_completed", False))

def _module_completed(user, module_id):
    lesson_ids = _lesson_ids_for_user_module(user, module_id)
    if not lesson_ids:
        return False
    user_id = _progress_user_id(user)
    completed_count = UserProgress.objects.filter(
        user_id=user_id,
        lesson_id__in=lesson_ids,
        completed=True,
    ).count()
    return completed_count == len(lesson_ids)

def _module_level_map(user):
    levels = {}
    mastery_vector = user.mastery_vector or {}
    difficulty_map = mastery_vector.get("_module_difficulty", {})
    
    # 1. Populate from mastery_vector (primary source)
    for key, val in difficulty_map.items():
        levels[key] = val
        # Handle string vs int IDs if any
        if key.isdigit():
            levels[int(key)] = val
        if key.replace("_", "-").replace("mod-", "").isdigit():
            try:
                levels[int(key.replace("_", "-").replace("mod-", ""))] = val
            except ValueError:
                pass
            
    # 2. Overlay from QuizAttempt notes (legacy/manual)
    attempts = QuizAttempt.objects.filter(user=user).order_by("completed_at")
    for attempt in attempts:
        match = re.search(r"module:(\d+):level:([A-Za-z]+)", attempt.notes or "")
        if match:
            levels[int(match.group(1))] = match.group(2)
            
    # 3. Handle special diagnostic module name mappings
    intro_val = difficulty_map.get("mod_introduction") or difficulty_map.get("mod-introduction")
    if intro_val:
        levels["mod-python-basics"] = intro_val
        
    var_val = difficulty_map.get("mod_variables_types") or difficulty_map.get("mod-variables-types")
    if var_val:
        levels["mod-variables-types"] = var_val

    return levels

def _normalize_level(level):
    lower = (level or "").strip().lower()
    if lower == "pro" or lower == "advanced":
        return "Pro"  # Database uses "Pro"
    if lower == "intermediate":
        return "Intermediate"
    return "Beginner"

def _lesson_ids_for_user_module(user, module_id):
    """
    Returns lesson IDs for the user filtered by their assigned difficulty level.
    """
    mastery_vector = user.mastery_vector or {}
    difficulty_map = mastery_vector.get("_module_difficulty", {}).copy()
    
    # Add reverse mappings from diagnostic quiz keys to actual module IDs
    reverse_mappings = {
        "mod_introduction": "mod-python-basics",
        "mod_variables_types": "mod-data-types",
        "mod_control_flow": "mod-control-flow",
        "mod_loops_iteration": "mod-control-flow",
        "mod_functions_scope": "mod-functions",
        "mod_file_handling": "mod-modules-packages",
        "mod_error_handling": "mod-modules-packages",
    }
    for alias_key, target_module in reverse_mappings.items():
        if alias_key in difficulty_map:
            difficulty_map[target_module] = difficulty_map[alias_key]
            difficulty_map[target_module.replace("-", "_")] = difficulty_map[alias_key]
    
    # Find the assigned difficulty for this module
    mod_id = str(module_id)
    search_keys = [mod_id, mod_id.replace("-", "_")]
    special_mappings = {
        "mod-python-basics": ["mod_introduction", "mod-introduction"],
        "mod-data-types": ["mod_variables_types", "mod-variables-types"],
        "mod-control-flow": ["mod_control_flow", "mod_loops_iteration", "mod-loops-iteration"],
        "mod-functions": ["mod_functions_scope", "mod-functions-scope"],
        "mod-modules-packages": ["mod_file_handling", "mod_error_handling", "mod-file-handling", "mod-error-handling"],
    }
    if mod_id in special_mappings:
        search_keys.extend(special_mappings[mod_id])
    
    assigned_difficulty = None
    for sk in search_keys:
        if sk in difficulty_map:
            assigned_difficulty = difficulty_map[sk]
            break
    
    # Map to database difficulty value
    if assigned_difficulty:
        target_difficulty = map_level_to_db(assigned_difficulty)
    else:
        target_difficulty = map_level_to_db(user.level or "Beginner")
    
    # Return lessons filtered by difficulty
    lessons = Lesson.objects.filter(module_id=module_id, difficulty=target_difficulty).order_by('order')
    if lessons.exists():
        return list(lessons.values_list("id", flat=True))
    
    # Fallback: return all lessons if no lessons match the target difficulty
    return list(Lesson.objects.filter(module_id=module_id).order_by('order').values_list("id", flat=True))

def _prerequisites_met(user, lesson_id: str) -> bool:
    profile = LessonProfile.objects.filter(lesson_id=str(lesson_id)).first()
    prereqs = list((profile.prerequisites or []) if profile else [])
    if not prereqs:
        return True
    
    # prereqs may be list of strings (slugs) or ints (legacy)
    prereq_ids = [str(val) for val in prereqs]
    
    if not prereq_ids:
        return True
    user_id = _progress_user_id(user)
    completed_ids = set(
        UserProgress.objects.filter(user_id=user_id, lesson_id__in=prereq_ids, completed=True)
        .values_list("lesson_id", flat=True)
    )
    return all(pid in completed_ids for pid in prereq_ids)

def _module_unlocked(user, module):
    # Allow access to the first module for new users even if they haven't completed the placement quiz yet.
    # This prevents the app from appearing empty on first login.
    if module.order == 1:
        return True
    if not _quiz_completed(user):
        return False
    previous_module = Module.objects.filter(order=module.order - 1).first()
    if not previous_module:
        return True
    # If the previous module has no lessons yet (e.g. during early seeding),
    # treat it as transparently completed so that later modules with real
    # lessons can still unlock for the user.
    if not Lesson.objects.filter(module_id=previous_module.id).exists():
        return True
    return _module_completed(user, previous_module.id)

def _lesson_unlocked(user, lesson):
    if not _quiz_completed(user):
        # Allow first lesson of first module even without quiz
        module = Module.objects.filter(id=lesson.module_id).first()
        if module and module.order == 1 and lesson.order == 1:
            return True
        return False
    module = Module.objects.filter(id=lesson.module_id).first()
    if not module or not _module_unlocked(user, module):
        return False
    
    # If it's the first lesson of a module, it's unlocked if module is unlocked
    if lesson.order == 1:
        return _prerequisites_met(user, lesson.id)

    user_id = _progress_user_id(user)
    # Check if ANY version of the previous lesson (order - 1) is completed
    prev_order = lesson.order - 1
    previous_lessons = Lesson.objects.filter(module_id=lesson.module_id, order=prev_order)
    
    sequential_ok = False
    if previous_lessons.exists():
        prev_ids = list(previous_lessons.values_list("id", flat=True))
        sequential_ok = UserProgress.objects.filter(
            user_id=user_id,
            lesson_id__in=prev_ids,
            completed=True,
        ).exists()
    else:
        # If no previous lesson exists with order-1, it might be the first available
        sequential_ok = True
    
    return sequential_ok and _prerequisites_met(user, lesson.id)

def _unlocked_module_ids(user):
    if not _quiz_completed(user):
        return []
    modules = list(Module.objects.all().order_by("order"))
    unlocked_ids = []
    for module in modules:
        # Skip modules that currently have no lessons configured so they don't
        # block access to later modules that do have real content.
        if not Lesson.objects.filter(module_id=module.id).exists():
            continue
        if _module_unlocked(user, module):
            unlocked_ids.append(module.id)
        else:
            break
    return unlocked_ids

def _unlocked_lesson_ids(user):
    unlocked_modules = _unlocked_module_ids(user)
    if not unlocked_modules:
        return []
    user_id = _progress_user_id(user)
    unlocked_ids = []
    for module_id in unlocked_modules:
        lesson_ids = _lesson_ids_for_user_module(user, module_id)
        lessons = list(Lesson.objects.filter(id__in=lesson_ids).order_by("order"))
        completed_ids = set(UserProgress.objects.filter(
            user_id=user_id,
            lesson_id__in=[lesson.id for lesson in lessons],
            completed=True,
        ).values_list("lesson_id", flat=True))
        for lesson in lessons:
            # Find previous lesson in the current module's ordered list
            previous = next((l for l in reversed(lessons) if l.order < lesson.order), None)
            if (not previous or previous.id in completed_ids) and _prerequisites_met(user, lesson.id):
                unlocked_ids.append(lesson.id)
    return unlocked_ids

def get_advanced_variant(module_id, base_lesson):
    if not base_lesson:
        return None
    current = (getattr(base_lesson, "difficulty", "") or "").strip().lower()
    if current in ("pro", "advanced"):
        return None
    return Lesson.objects.filter(
        module_id=module_id,
        slug=base_lesson.slug,
        order=base_lesson.order,
        difficulty="Pro",
    ).first()

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
        except Exception as e:
            # Format validation errors into a single message string
            error_messages = []
            if hasattr(e, 'detail'):
                for field, errors in e.detail.items():
                    if isinstance(errors, list):
                        error_messages.extend([f"{field}: {error}" for error in errors])
                    else:
                        error_messages.append(f"{field}: {errors}")
            if not error_messages:
                error_messages.append(str(e) if str(e) else "Registration failed due to invalid data.")
            return Response({'message': '; '.join(error_messages)}, status=status.HTTP_400_BAD_REQUEST)

        # Generate JWT tokens for immediate login
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        
        response_data = serializer.data
        response_data['access'] = str(refresh.access_token)
        response_data['refresh'] = str(refresh)
        
        return Response(response_data, status=status.HTTP_201_CREATED)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        identifier = request.data.get('identifier') or request.data.get('email') or request.data.get('username')
        password = request.data.get('password')
        if not identifier or not password:
            return Response({'message': 'Identifier and password are required'}, status=400)
        if "@" in identifier:
            target_user = User.objects.filter(email__iexact=identifier).first()
            username = target_user.username if target_user else identifier
        else:
            username = identifier
        user = authenticate(request, username=username, password=password)

        if user:
            # login(request, user) # Removed to avoid session/CSRF issues with JWT
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            })
        return Response({'message': 'Invalid credentials'}, status=401)

class UserProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """Get user profile information"""
        return Response(UserSerializer(request.user).data)

    def post(self, request):
        """Handle profile updates and avatar uploads based on URL path"""
        if request.path.endswith('/avatar'):
            return self.handle_avatar_upload(request)
        elif request.path.endswith('/update'):
            return self.handle_profile_update(request)
        else:
            # Default behavior for backward compatibility
            return self.handle_profile_update(request)

    def handle_profile_update(self, request):
        """Handle profile information updates"""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            # Format validation errors into a single message string
            error_messages = []
            if hasattr(e, 'detail'):
                for field, errors in e.detail.items():
                    if isinstance(errors, list):
                        error_messages.extend([f"{field}: {error}" for error in errors])
                    else:
                        error_messages.append(f"{field}: {errors}")
            if not error_messages:
                error_messages.append("Profile update failed due to invalid data.")
            return Response({'message': '; '.join(error_messages)}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    def handle_avatar_upload(self, request):
        """Handle profile image upload"""
        if 'profile_image' not in request.FILES:
            return Response({'message': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        profile_image = request.FILES['profile_image']
        
        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if profile_image.content_type not in allowed_types:
            return Response({'message': 'Invalid image type. Allowed: JPEG, PNG, GIF, WebP'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate file size (5MB limit)
        if profile_image.size > 5 * 1024 * 1024:
            return Response({'message': 'Image size must be less than 5MB'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Save the image to the user's profile
            request.user.profileImageUrl = profile_image
            request.user.save()
            
            return Response({
                'profileImageUrl': request.user.profileImageUrl.url if request.user.profileImageUrl else None
            })
        except Exception as e:
            return Response({'message': f'Failed to upload image: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        """Handle profile updates - kept for compatibility but POST is preferred"""
        return self.post(request)  # Use the same logic as POST

    def patch(self, request):
        """Handle partial profile updates - kept for compatibility but POST is preferred"""
        return self.post(request)  # Use the same logic as POST

class LogoutView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def get(self, request):
        logout(request)
        return Response({'message': 'Logged out'})

class RunChallengeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def strip_input_prompts(self, code, text):
        import re
        if not text:
            return ""
        # Collect explicit prompt strings used in input() calls
        prompt_matches = re.findall(r"input\s*\(\s*(['\"])(.*?)\1\s*\)", code)
        cleaned = text
        for _, prompt in prompt_matches:
            if prompt:
                # Replace all prompt occurrences from output so match is based on logical result
                cleaned = cleaned.replace(prompt, "")
        return cleaned.strip()

    def _is_numeric(self, text):
        try:
            float(text)
            return True
        except Exception:
            return False

    def _extract_numeric_tokens(self, text):
        return re.findall(r"-?\d+\.?\d*", text)

    def is_output_equivalent(self, expected, actual):
        expected = (expected or "").strip()
        actual = (actual or "").strip()
        if expected == actual:
            return True

        # Exact word in actual (for player-friendly annotated output)
        if expected and re.search(rf"\b{re.escape(expected)}\b", actual):
            return True

        # Numeric tolerance for cases like `sum: 15` vs `15`.
        if self._is_numeric(expected) and self._is_numeric(actual):
            try:
                return float(expected) == float(actual)
            except Exception:
                pass

        if self._is_numeric(expected):
            actual_tokens = self._extract_numeric_tokens(actual)
            if actual_tokens and actual_tokens[-1] == expected:
                return True

        return False

    def post(self, request, id):
        code = request.data.get('code', '')
        input_text = request.data.get('input', '')
        if not code.strip():
            return Response({'message': 'Please write some code before running.'}, status=status.HTTP_400_BAD_REQUEST)

        def run_code(code_to_run, input_text=""):
            filename = f"temp_{uuid.uuid4()}.py"
            # Use a more reliable temp directory
            temp_dir = os.path.join(tempfile.gettempdir(), 'great_design_tmp')
            os.makedirs(temp_dir, exist_ok=True)
            filepath = os.path.join(temp_dir, filename)
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(code_to_run)
                # Quote the executable on Windows if it contains spaces
                executable = sys.executable
                
                # Handle input if provided
                if input_text:
                    # Ensure input has trailing newline for Python's input() function
                    if not input_text.endswith('\n'):
                        input_text += '\n'
                    result = subprocess.run(
                        [executable, filepath],
                        input=input_text,
                        capture_output=True,
                        text=True,
                        timeout=5,
                        cwd=temp_dir,
                        encoding='utf-8'
                    )
                else:
                    result = subprocess.run(
                        [executable, filepath],
                        capture_output=True,
                        text=True,
                        timeout=5,
                        cwd=temp_dir,
                        encoding='utf-8'
                    )
                if "ModuleNotFoundError" in result.stderr:
                    module_name = result.stderr.split("'")[1]
                    return result.stdout, f"Error: Module '{module_name}' not found. Please import a valid module."
                return result.stdout, result.stderr
            finally:
                if os.path.exists(filepath):
                    try:
                        os.remove(filepath)
                    except Exception:
                        pass

        try:
            challenge = Challenge.objects.get(id=id)
        except Challenge.DoesNotExist:
            return Response({'message': 'Challenge not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Execute tests. If test_cases contain inputs, run per case and compare outputs
            test_cases = challenge.test_cases if challenge.test_cases else []
            all_passed = True
            error_message = None
            combined_output = ""

            temp_dir = os.path.join(tempfile.gettempdir(), 'great_design_tmp')
            os.makedirs(temp_dir, exist_ok=True)

            if test_cases and not input_text:
                for tc in test_cases:
                    tc_input = str(tc.get("input") or "")
                    if tc_input and not tc_input.endswith('\n'):
                        tc_input += '\n'
                    filename = f"temp_{uuid.uuid4()}.py"
                    filepath = os.path.join(temp_dir, filename)
                    try:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(code)
                        executable = sys.executable
                        result = subprocess.run(
                            [executable, filepath],
                            input=tc_input,
                            capture_output=True,
                            text=True,
                            timeout=5,
                            cwd=temp_dir,
                            encoding='utf-8'
                        )
                        out = result.stdout.strip()
                        err = result.stderr.strip()

                        cleaned_out = self.strip_input_prompts(code, out)
                        combined_output += cleaned_out + ("\n" if cleaned_out else "")

                        expected = str(tc.get("expected", "")).strip()
                        if err or not self.is_output_equivalent(expected, cleaned_out):
                            all_passed = False
                            if err:
                                error_message = err
                            else:
                                error_message = f"Expected '{expected}', got '{cleaned_out}'"
                            break
                    except subprocess.TimeoutExpired:
                        all_passed = False
                        error_message = "Execution timed out"
                        break
                    finally:
                        if os.path.exists(filepath):
                            try:
                                os.remove(filepath)
                            except Exception:
                                pass
            else:
                # Fallback to single run and optional comparison with reference solution
                stdout, stderr = run_code(code, input_text)
                cleaned_stdout = self.strip_input_prompts(code, stdout.strip())
                combined_output = cleaned_stdout
                if stderr:
                    all_passed = False
                    error_message = stderr
                elif challenge.solution_code:
                    expected_stdout, expected_stderr = run_code(challenge.solution_code, input_text)
                    cleaned_expected = self.strip_input_prompts(challenge.solution_code, expected_stdout.strip())
                    if expected_stderr:
                        all_passed = False
                        error_message = "Reference solution failed to run"
                    else:
                        all_passed = self.is_output_equivalent(cleaned_expected, cleaned_stdout)
                        if not all_passed:
                            error_message = f"Expected '{cleaned_expected}', got '{cleaned_stdout}'"

            if challenge and challenge.lesson_id:
                lesson = Lesson.objects.filter(id=challenge.lesson_id).first()
                if lesson:
                    topic = LessonProfile.objects.filter(lesson_id=lesson.id).values_list("topic", flat=True).first() or lesson.title
                    log_assessment_interaction(request.user, topic, all_passed, 0, 0, "challenge")
                    update_engagement(request.user, 0.01 if all_passed else -0.01)
                    
                    if all_passed:
                        user_id = request.user.original_uuid or str(request.user.id)
                        progress, _ = UserProgress.objects.get_or_create(user_id=user_id, lesson_id=lesson.id)
                        progress.challenge_completed = True
                        # Overall completion only if quiz is also done
                        if progress.quiz_completed:
                            progress.completed = True
                            if not progress.completed_at:
                                progress.completed_at = timezone.now()
                        progress.save()
                        logger.info(f"Challenge completed for user {request.user.id}, lesson {lesson.id}")
            return Response({
                'output': combined_output,
                'error': error_message,
                'passed': all_passed
            })

        except subprocess.TimeoutExpired:
            return Response({
                'output': '',
                'error': 'Execution timed out',
                'passed': False
            }, status=status.HTTP_408_REQUEST_TIMEOUT)
        except Exception as e:
            return Response({
                'output': '',
                'error': str(e),
                'passed': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            try:
                analyze_user_skill_gaps(request.user)
            except Exception:
                pass


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all().order_by('order')
    serializer_class = ModuleSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = self.request.user
        if not user or not user.is_authenticated:
            return context
            
        # Pre-calculate all module difficulties once to avoid N+1 queries in ModuleSerializer
        mastery_vector = user.mastery_vector or {}
        diff_map = mastery_vector.get("_module_difficulty", {}).copy()
        
        # Add reverse mappings from diagnostic quiz keys to module IDs
        # This ensures lookups work when mastery vector uses different keys than module IDs
        reverse_mappings = {
            "mod_introduction": "mod-python-basics",
            "mod_variables_types": "mod-data-types",
            "mod_control_flow": "mod-control-flow",
            "mod_loops_iteration": "mod-control-flow",
            "mod_functions_scope": "mod-functions",
            "mod_file_handling": "mod-modules-packages",
            "mod_error_handling": "mod-modules-packages",
        }
        for alias_key, target_module in reverse_mappings.items():
            if alias_key in diff_map:
                diff_map[target_module] = diff_map[alias_key]
                diff_map[target_module.replace("-", "_")] = diff_map[alias_key]
        
        # Merge with legacy quiz attempt notes to ensure consistency (same logic as Serializer)
        from .models import QuizAttempt as CoreQuizAttempt
        import re
        attempts = CoreQuizAttempt.objects.filter(user=user).order_by("completed_at")
        for attempt in attempts:
            notes = attempt.notes or ""
            match = re.search(r"module:([\w-]+):level:([A-Za-z]+)", notes)
            if match:
                m_id = match.group(1).lower()
                lvl = match.group(2)
                diff_map[m_id] = lvl
                diff_map[m_id.replace("-", "_")] = lvl
                # Also add reverse mapping
                if m_id in reverse_mappings:
                    target = reverse_mappings[m_id]
                    diff_map[target] = lvl
                    diff_map[target.replace("-", "_")] = lvl
                
        context["precalculated_difficulties"] = diff_map
        return context

    def get_queryset(self):
        # Return all modules; serializer controls lesson visibility based on unlocks
        return self.queryset.order_by("order")

    def retrieve(self, request, *args, **kwargs):
        module = Module.objects.filter(id=kwargs.get("pk")).first()
        if not module:
            return Response({"message": "Module not found"}, status=status.HTTP_404_NOT_FOUND)
        if not _module_unlocked(request.user, module):
            return Response({"message": "You need to complete the placement quiz to personalize your learning path."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(module)
        return Response(serializer.data)

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all().order_by('order')
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Always allow viewing the lesson if it's explicitly requested by ID or in retrieve action
        # (This avoids 404s when following valid dashboard links)
        if self.action == 'retrieve' or self.kwargs.get('pk'):
            return self.queryset.all()
        
        user = self.request.user
        if not user or not user.is_authenticated:
            return self.queryset.none()
            
        # Filter lessons by user's unlocked path
        unlocked_ids = _unlocked_lesson_ids(user)
        return self.queryset.filter(id__in=unlocked_ids).order_by("order")

    def retrieve(self, request, *args, **kwargs):
        lesson = Lesson.objects.filter(id=kwargs.get("pk")).first()
        if not lesson:
            logger.warning(f"Lesson not found: {kwargs.get('pk')}")
            return Response({"message": "Lesson not found"}, status=status.HTTP_404_NOT_FOUND)
        # Bypassing _lesson_unlocked check for direct ID requests to ensure access from dashboard
        try:
            # Fix: Ensure Question import is available if needed
            from .models import Quiz, Question
            has_quiz = Quiz.objects.filter(lesson_id=lesson.id).exists()
            if not has_quiz:
                generated = generate_quiz_from_lesson(lesson)
                if generated:
                    quiz, _ = Quiz.objects.get_or_create(lesson_id=lesson.id, title=f"{lesson.title} Quiz (AI Generated)")
                    for item in generated:
                        text = item.get("question") or ""
                        options_arr = []
                        for idx, opt_text in enumerate(item.get("options") or []):
                            options_arr.append({"text": opt_text, "correct": idx == int(item.get("correct", -1))})
                        if text and options_arr:
                            Question.objects.get_or_create(
                                quiz_id=quiz.id,
                                text=text,
                                defaults={"type": "mcq", "options": options_arr, "points": 1},
                            )
                    logger.info(f"Generated quiz for lesson {lesson.id}")
        except Exception as e:
            logger.error(f"Error generating quiz for lesson {lesson.id}: {e}")
        serializer = self.get_serializer(lesson)
        return Response(serializer.data)

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = (permissions.IsAdminUser,)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAdminUser,)

class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UserProgressViewSet(viewsets.ModelViewSet):
    queryset = UserProgress.objects.all()
    serializer_class = UserProgressSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Filter by original_uuid if present (for migrated users)
        # OR by id if we start using int IDs. 
        # But UserProgress table has `user_id` as text.
        # So we must use original_uuid if it exists.
        user = self.request.user
        if user.original_uuid:
            return self.queryset.filter(user_id=user.original_uuid)
        return self.queryset.filter(user_id=str(user.id))

    def create(self, request, *args, **kwargs):
        # Removed placement quiz check to allow progress updates
        # Auto-populate userId from authenticated user
        user = request.user
        user_id = user.original_uuid or str(user.id)
        
        # Prepare data with userId populated (serializer expects camelCase field name)
        data = request.data.copy()
        data['userId'] = user_id
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        lesson_id = serializer.validated_data.get("lesson_id")
        completed = serializer.validated_data.get("completed")
        score = serializer.validated_data.get("score")
        last_code = serializer.validated_data.get("last_code")
        completed_at = serializer.validated_data.get("completed_at")
        time_spent = request.data.get("timeSpent", 0)
        hints_used = request.data.get("hintsUsed", 0)
        if completed and not completed_at:
            completed_at = timezone.now()

        progress, created = UserProgress.objects.get_or_create(
            user_id=user_id,
            lesson_id=lesson_id,
        )
        
        quiz_completed_val = serializer.validated_data.get("quiz_completed")
        challenge_completed_val = serializer.validated_data.get("challenge_completed")

        # Update fields only if they are provided or we are in a 'safe' state
        if score is not None:
            progress.score = score
        if last_code is not None:
            progress.last_code = last_code
        if completed_at:
            progress.completed_at = completed_at
        if quiz_completed_val is not None:
            progress.quiz_completed = quiz_completed_val
        if challenge_completed_val is not None:
            progress.challenge_completed = challenge_completed_val
            
        # Overall completion is ONLY True if both sub-flags are True
        # (Though we trust the backend views more for these flags)
        if progress.quiz_completed and progress.challenge_completed:
            progress.completed = True
            if not progress.completed_at:
                progress.completed_at = timezone.now()
        else:
            progress.completed = False
            
        progress.save()
        lesson = Lesson.objects.filter(id=lesson_id).first()
        topic = None
        if lesson:
            topic = LessonProfile.objects.filter(lesson_id=lesson.id).values_list("topic", flat=True).first() or lesson.title
            mark_recommendation_accepted(user, lesson.id)
        if completed:
            if lesson:
                mastery_before = float((user.mastery_vector or {}).get(topic, 0)) if topic else None
                log_assessment_interaction(user, topic, True, float(time_spent or 0), int(hints_used or 0), "lesson")
                update_engagement(user, 0.02)
                add_xp(user, 10, "Lesson completed")
                update_streak(user)
                mastery_after = None
                if score is not None:
                    mastery_after = update_user_mastery(user, lesson.module_id, float(score), "lesson", topic=topic)
                if mastery_after is None and topic:
                    mastery_after = float((user.mastery_vector or {}).get(topic, 0))
                mark_recommendation_completed(user, lesson.id, mastery_before, mastery_after)
                if topic:
                    update_shift_outcome(user, topic, mastery_before, mastery_after)
                
                # Logic to unlock the next lesson immediately
                # Get lessons matching user's difficulty level for proper sequencing
                target_difficulty = (lesson.difficulty or user.level or "Beginner").strip()
                
                # Get lessons in this module filtered by user's difficulty level
                lessons_in_module = Lesson.objects.filter(
                    module_id=lesson.module_id, 
                    difficulty=target_difficulty
                ).order_by('order')
                lesson_list = list(lessons_in_module)
                
                try:
                    current_idx = -1
                    for i, l in enumerate(lesson_list):
                        if str(l.id) == str(lesson.id):
                            current_idx = i
                            break
                    
                    if current_idx != -1 and current_idx + 1 < len(lesson_list):
                        next_lesson = lesson_list[current_idx + 1]
                        # Pre-create progress for next lesson if it doesn't exist
                        # This marks it as "unlocked" in UI logic
                        UserProgress.objects.get_or_create(
                            user_id=user_id,
                            lesson_id=str(next_lesson.id),
                            defaults={"completed": False}
                        )
                except Exception as e:
                    logger.error(f"Error unlocking next lesson: {str(e)}")
                    pass

                lesson_ids = list(lessons_in_module.values_list("id", flat=True))
                if lesson_ids:
                    completed_count = UserProgress.objects.filter(
                        user_id=user_id,
                        lesson_id__in=lesson_ids,
                        completed=True,
                    ).count()
                    total_completed = UserProgress.objects.filter(user_id=user_id, completed=True).count()
                    if total_completed >= 10:
                        award_badge(user, "consistent-learner")
                    if completed_count == len(lesson_ids):
                        module = Module.objects.filter(id=lesson.module_id).first()
                        module_title = module.title if module else f"Module {lesson.module_id}"
                        Certificate.objects.get_or_create(
                            user=user,
                            module=module_title,
                            defaults={
                                "pdf_path": f"/certificate/{lesson.module_id}",
                            },
                        )
        output = self.get_serializer(progress).data
        return Response(output, status=status.HTTP_200_OK)


class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        """Override list to return empty progress for new users"""
        queryset = self.get_queryset()
        
        # Return existing progress only - no auto-creation for new users
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class DiagnosticSubmitView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        quiz_id = request.data.get("quizId")
        answers = request.data.get("answers", [])
        if not quiz_id or not isinstance(answers, list):
            return Response({"message": "quizId and answers are required"}, status=status.HTTP_400_BAD_REQUEST)

        questions = list(Question.objects.filter(quiz_id=quiz_id))
        if not questions:
            return Response({"message": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

        answers_map = {}
        for answer in answers:
            q_id = answer.get("questionId")
            selected_index = answer.get("selectedIndex")
            if q_id is not None:
                # Convert to string to match Question.id (which is a CharField)
                answers_map[str(q_id)] = selected_index

        module_totals = {}
        module_correct = {}
        total_questions = 0
        correct_answers = 0

        for question in questions:
            # question.id is already a string
            meta = DiagnosticQuestionMeta.objects.filter(question_id=question.id).first()
            if not meta:
                continue
            module_tag = meta.module_tag
            options = question.options or []
            correct_index = None
            for idx, opt in enumerate(options):
                if opt.get("correct"):
                    correct_index = idx
                    break
            total_questions += 1
            module_totals[module_tag] = module_totals.get(module_tag, 0) + 1
            selected_index = answers_map.get(question.id)
            if selected_index is not None and correct_index is not None and int(selected_index) == int(correct_index):
                correct_answers += 1
                module_correct[module_tag] = module_correct.get(module_tag, 0) + 1

        if total_questions == 0:
            return Response({"message": "No diagnostic questions available"}, status=status.HTTP_400_BAD_REQUEST)

        module_scores = {}
        for module_tag, total in module_totals.items():
            score = (module_correct.get(module_tag, 0) / total) * 100
            module_scores[module_tag] = round(score, 2)

        overall_score = round((correct_answers / total_questions) * 100, 2)

        DiagnosticAttempt.objects.create(
            user=request.user,
            quiz_id=quiz_id,
            module_scores=module_scores,
            overall_score=overall_score,
        )

        for module_tag, score in module_scores.items():
            module = Module.objects.filter(title__iexact=module_tag).first()
            if module:
                update_user_mastery(request.user, module.id, score, "diagnostic")
        request.user.diagnostic_completed = True
        request.user.has_taken_quiz = True
        request.user.save(update_fields=["diagnostic_completed", "has_taken_quiz"])

        return Response({
            "moduleScores": module_scores,
            "overallScore": overall_score,
            "masteryVector": request.user.mastery_vector or {},
        })

class MasteryUpdateView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        module_id = request.data.get("moduleId")
        score = request.data.get("score")
        source = request.data.get("source", "activity")
        topic = request.data.get("topic")
        if module_id is None or score is None:
            return Response({"message": "moduleId and score are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            module_id = int(module_id)
            score = float(score)
        except (TypeError, ValueError):
            return Response({"message": "Invalid moduleId or score"}, status=status.HTTP_400_BAD_REQUEST)

        update_user_mastery(request.user, module_id, score, source, topic=topic)
        return Response({"masteryVector": request.user.mastery_vector or {}})

class AdaptiveRecommendationView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        if not _quiz_completed(request.user):
            return Response(
                {"message": "You need to complete the placement quiz to personalize your learning path."},
                status=status.HTTP_403_FORBIDDEN,
            )
        modules = list(Module.objects.all().order_by('order'))
        if not modules:
            return Response({"message": "No modules available"}, status=status.HTTP_404_NOT_FOUND)

        mastery_map = {m.module_id: m.mastery_score for m in UserMastery.objects.filter(user=request.user)}
        target_module = None
        target_score = None
        for module in modules:
            score = mastery_map.get(module.id, 0)
            if target_score is None or score < target_score:
                target_module = module
                target_score = score

        if target_module is None:
            target_module = modules[0]
            target_score = 0

        module_lessons = list(Lesson.objects.filter(module_id=target_module.id).values_list("id", flat=True))
        advanced_override = None
        if module_lessons:
            user_id = request.user.original_uuid or str(request.user.id)
            last_progress = UserProgress.objects.filter(
                user_id=user_id,
                lesson_id__in=module_lessons,
                completed=True,
            ).order_by('-completed_at').first()
            if last_progress and last_progress.score is not None and float(last_progress.score) >= 80:
                base_lesson = Lesson.objects.filter(id=last_progress.lesson_id).first()
                if base_lesson and (base_lesson.difficulty or "").lower() in ["beginner", "intermediate"]:
                    candidate = get_advanced_variant(target_module.id, base_lesson)
                    if candidate:
                        already_done = UserProgress.objects.filter(
                            user_id=user_id,
                            lesson_id=candidate.id,
                            completed=True,
                        ).exists()
                        if not already_done:
                            advanced_override = candidate

        difficulty_level = normalize_level_for_score(target_score)
        db_level = map_level_to_db(difficulty_level)
        if difficulty_level == "Advanced":
            advanced_completed = is_level_completed(request.user, target_module.id, db_level)
            if advanced_completed and target_score > 80:
                current_index = next((idx for idx, m in enumerate(modules) if m.id == target_module.id), 0)
                if current_index + 1 < len(modules):
                    target_module = modules[current_index + 1]
                    target_score = mastery_map.get(target_module.id, 0)
                    difficulty_level = normalize_level_for_score(target_score)
                    db_level = map_level_to_db(difficulty_level)

        if advanced_override:
            lessons = [advanced_override]
            next_lesson = advanced_override
            topic = LessonProfile.objects.filter(lesson_id=next_lesson.id).values_list("topic", flat=True).first() or next_lesson.title
            log_recommendation_event(
                user=request.user,
                algorithm_name="adaptive_mastery",
                recommended_lesson_id=next_lesson.id,
                recommended_topic=topic,
                confidence=0.7,
            )
            behavior = get_behavior(request.user, topic)
            adjustment = compute_difficulty_adjustment(float(mastery_map.get(target_module.id, 0)), behavior, next_lesson.difficulty or "Beginner")
            log_difficulty_shift(
                request.user,
                topic,
                next_lesson.difficulty or "Beginner",
                adjustment["target"],
                behavior,
                float(mastery_map.get(target_module.id, 0)),
                reason=adjustment["reason"],
            )
            return Response({
                "nextModule": {
                    "id": target_module.id,
                    "title": target_module.title,
                    "order": target_module.order,
                },
                "difficultyLevel": "Advanced",
                "nextLesson": {
                    "id": next_lesson.id,
                    "title": next_lesson.title,
                    "order": next_lesson.order,
                },
                "lessons": [
                    {"id": next_lesson.id, "title": next_lesson.title, "order": next_lesson.order, "difficulty": next_lesson.difficulty}
                ],
                "strategy": get_or_assign_strategy(request.user).strategy_name,
                "algorithm": "adaptive_mastery",
                "difficultyOverride": adjustment["target"] if adjustment["target"] != (next_lesson.difficulty or "Beginner") else None,
            })

        lessons_qs = Lesson.objects.filter(module_id=target_module.id, difficulty=db_level).order_by('order', 'id')
        if not lessons_qs.exists():
            lessons_qs = Lesson.objects.filter(module_id=target_module.id).order_by('order', 'id')
        lessons = list(lessons_qs[:5])
        next_lesson = lessons[0] if lessons else None

        adjustment = {"target": None}
        if next_lesson:
            topic = LessonProfile.objects.filter(lesson_id=next_lesson.id).values_list("topic", flat=True).first() or next_lesson.title
            behavior = get_behavior(request.user, topic)
            adjustment = compute_difficulty_adjustment(float(mastery_map.get(target_module.id, 0)), behavior, next_lesson.difficulty or "Beginner")
            log_difficulty_shift(
                request.user,
                topic,
                next_lesson.difficulty or "Beginner",
                adjustment["target"],
                behavior,
                float(mastery_map.get(target_module.id, 0)),
                reason=adjustment["reason"],
            )
            if adjustment["target"] == "Challenge":
                candidate = get_advanced_variant(target_module.id, next_lesson)
                if candidate:
                    next_lesson = candidate
            log_recommendation_event(
                user=request.user,
                algorithm_name="adaptive_mastery",
                recommended_lesson_id=next_lesson.id,
                recommended_topic=topic,
                confidence=0.7,
            )
        return Response({
            "nextModule": {
                "id": target_module.id,
                "title": target_module.title,
                "order": target_module.order,
            },
            "difficultyLevel": difficulty_level,
            "nextLesson": {
                "id": next_lesson.id,
                "title": next_lesson.title,
                "order": next_lesson.order,
            } if next_lesson else None,
            "lessons": [
                {"id": lesson.id, "title": lesson.title, "order": lesson.order, "difficulty": lesson.difficulty}
                for lesson in lessons
            ],
            "strategy": get_or_assign_strategy(request.user).strategy_name,
            "algorithm": "adaptive_mastery",
            "difficultyOverride": adjustment["target"] if next_lesson and adjustment["target"] != (next_lesson.difficulty or "Beginner") else None,
        })


class QuizAttemptViewSet(viewsets.ModelViewSet):
    queryset = QuizAttempt.objects.all()
    serializer_class = QuizAttemptSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        notes = request.data.get("notes", "")
        score = request.data.get("score", 0)
        topic = request.data.get("topic")
        correct = request.data.get("correct")
        time_spent = request.data.get("timeSpent", 0)
        hints_used = request.data.get("hintsUsed", 0)

        # Parse notes for module-level updates (e.g. "module:1:level:Pro")
        import re
        match = re.search(r"module:([^:]+):level:([A-Za-z]+)", notes)
        if match:
            module_id = match.group(1)
            # Update the user's mastery vector so the backend knows to serve correctly
            # normalize_level_for_score is called inside update_user_mastery
            update_user_mastery(request.user, module_id, score, "module_quiz")
            logger.info(f"Updated mastery vector for user {request.user.id}, module {module_id} from quiz notes.")

        if topic is not None and correct is not None:
            log_assessment_interaction(request.user, topic, bool(correct), float(time_spent or 0), int(hints_used or 0), "quiz")
        
        analyze_user_skill_gaps(request.user)
        output = serializer.data
        return Response(output, status=status.HTTP_200_OK)


class SubmitQuizView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, quiz_id):
        # quiz_id is expected as a string slug (e.g., 'quiz-python-basics-1')
        logger.info(f"User {request.user.id} submitting quiz {quiz_id}")
        try:
            quiz = Quiz.objects.filter(id=str(quiz_id)).first()
            if not quiz:
                raise Quiz.DoesNotExist()
        except Quiz.DoesNotExist:
            logger.warning(f"Quiz not found: {quiz_id}")
            return Response({"message": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

        answers = request.data.get("answers", [])
        if not answers:
            logger.warning(f"No answers provided for quiz {quiz_id}")
            return Response({"message": "No answers provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already attempted this quiz
        existing_attempt = QuizAttempt.objects.filter(user=request.user, quiz=quiz).first()
        if existing_attempt:
            logger.info(f"User {request.user.id} already attempted quiz {quiz_id}")
            return Response({"message": "Quiz already attempted"}, status=status.HTTP_400_BAD_REQUEST)

        questions = Question.objects.filter(quiz_id=quiz.id)
        question_map = {q.id: q for q in questions}
        score = 0
        total_questions = len(questions)

        # Create QuizAttempt
        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=0,  # Will update after calculating
            total_questions=total_questions
        )
        logger.info(f"Created quiz attempt {attempt.id} for user {request.user.id}")

        # Process answers
        for answer in answers:
            q_id = answer.get("question_id")
            selected = answer.get("selected")
            if q_id in question_map:
                question = question_map[q_id]
                options = question.options or []
                is_correct = False
                if isinstance(options, list) and 0 <= selected < len(options):
                    is_correct = options[selected].get("correct", False)
                if is_correct:
                    score += 1
                # QuestionAttempt.objects.create(
                #     attempt=attempt,
                #     question=question,
                #     selected_option=selected,
                #     is_correct=is_correct
                # )

        # Update score
        attempt.score = score
        attempt.save()
        logger.info(f"Quiz attempt {attempt.id} completed with score {score}/{total_questions}")

        # Analyze skill gaps
        analyze_user_skill_gaps(request.user)

        # Update UserProgress - always mark quiz as completed regardless of score
        user = request.user
        user_id = user.original_uuid or str(user.id)
        quiz_percentage = round((score / total_questions) * 100, 2) if total_questions > 0 else 0
        
        # Always update progress when quiz is submitted (no minimum score requirement)
        progress, _ = UserProgress.objects.get_or_create(user_id=user_id, lesson_id=quiz.lesson_id)
        progress.quiz_completed = True
        progress.score = int(quiz_percentage) if total_questions > 0 else 100
        
        # Overall completion ONLY if challenge is also done
        if progress.challenge_completed:
            progress.completed = True
            if not progress.completed_at:
                progress.completed_at = timezone.now()
        progress.save()
        logger.info(f"Quiz completed for user {user.id}, lesson {quiz.lesson_id}, score: {quiz_percentage}%")

        return Response({
            "score": score,
            "total": total_questions,
            "percentage": quiz_percentage,
            "passed": True
        })


class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class BadgeViewSet(viewsets.ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class CertificateDownloadView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, module_id):
        user = request.user
        module = Module.objects.filter(id=module_id).first()
        if module:
            certificate = Certificate.objects.filter(user=user, module=module.title).first()
        else:
            certificate = None

        if not certificate:
            return Response({"message": "Certificate not found"}, status=status.HTTP_404_NOT_FOUND)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="certificate_{user.username}_{module_id}.pdf"'

        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        # Certificate content
        p.setTitle(f"Certificate of Completion - {certificate.module}")
        p.setFont("Helvetica-Bold", 24)
        p.drawCentredString(width / 2.0, height - 2 * inch, "Certificate of Completion")

        p.setFont("Helvetica", 12)
        p.drawCentredString(width / 2.0, height - 3 * inch, "This certifies that")

        p.setFont("Helvetica-Bold", 20)
        p.drawCentredString(width / 2.0, height - 3.5 * inch, f"{user.first_name} {user.last_name}")

        p.setFont("Helvetica", 12)
        p.drawCentredString(width / 2.0, height - 4 * inch, f"has successfully completed the module")

        p.setFont("Helvetica-Bold", 16)
        p.drawCentredString(width / 2.0, height - 4.5 * inch, certificate.module)

        p.setFont("Helvetica", 10)
        p.drawCentredString(width / 2.0, 2 * inch, f"Issued on: {certificate.issued_at.strftime('%B %d, %Y')}")
        p.drawCentredString(width / 2.0, 1.5 * inch, f"Certificate ID: {certificate.id}")

        p.showPage()
        p.save()

        return response

class AITutorView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        message = request.data.get('message')
        if message is None:
            message = request.data.get('query', '')
        message = str(message).strip()
        if not message:
            return Response({'error': 'Query not provided'}, status=status.HTTP_400_BAD_REQUEST)

        topic = (request.data.get('topic') or 'general').strip() or 'general'
        history_payload = request.data.get('history') or []
        history_msgs = []
        if isinstance(history_payload, list):
            for m in history_payload[-5:]:
                try:
                    role = str(m.get('role')).lower()
                    content = str(m.get('content') or '').strip()
                    if role in ('user', 'assistant') and content:
                        history_msgs.append({'role': role, 'content': content})
                except Exception:
                    continue

        # Build messages (use provided history; if empty, consider last from session)
        session_key = f"aitutor_history:{topic}"
        session_hist = request.session.get(session_key, [])
        if not history_msgs and isinstance(session_hist, list):
            # Map stored session messages into OpenAI roles
            for m in session_hist[-5:]:
                try:
                    r = str(m.get('role')).lower()
                    c = str(m.get('content') or '').strip()
                    if r in ('user', 'assistant') and c:
                        history_msgs.append({'role': r, 'content': c})
                except Exception:
                    continue

        # Compose final payload
        system_message = {"role": "system", "content": "You are an expert Python tutor. Explain clearly, give examples, debug code, and answer based on context."}
        messages = [system_message] + history_msgs + [{"role": "user", "content": message}]

        # Prepare OpenRouter request
        api_key = os.environ.get("OPENAI_API_KEY")
        base_url = os.environ.get("OPENAI_BASE_URL", "https://openrouter.ai/api/v1").rstrip("/")
        model_id = os.environ.get("OPENAI_MODEL", "mistralai/mistral-7b-instruct")
        endpoint = f"{base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "AI Tutor Project",
        }
        payload = {
            "model": model_id,
            "messages": messages,
        }

        try:
            if not api_key:
                raise ValueError("Missing API key")
            req = urlreq.Request(endpoint, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
            timeout_seconds = int(os.environ.get("OPENAI_TIMEOUT_SECONDS", "20"))
            with urlreq.urlopen(req, timeout=timeout_seconds) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            assistant_text = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            if not assistant_text:
                return Response({"error": "AI service not available. Please try again later."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            session_key = f"aitutor_history:{topic}"
            session_hist = request.session.get(session_key, [])
            session_hist.append({'role': 'user', 'content': message})
            session_hist.append({'role': 'assistant', 'content': assistant_text})
            request.session[session_key] = session_hist[-10:]
            request.session.modified = True

            return Response({
                'response': assistant_text,
                'source': 'OpenRouter'
            })

        except urlerr.HTTPError as e:
            try:
                body = e.read().decode("utf-8")
            except Exception:
                body = ""
            logger.error(f"OpenRouter HTTPError {e.code}: {body}")
            return Response({"error": "AI service not available. Please try again later."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except (urlerr.URLError, ValueError, TimeoutError) as e:
            logger.error(f"OpenRouter request error: {e}")
            return Response({"error": "AI service not available. Please try again later."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            logger.error(f"OpenRouter unexpected error: {e}")
            return Response({"error": "AI service not available. Please try again later."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class ModuleQuizView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, module_id):
        user = request.user
        module = Module.objects.filter(id=module_id).first()
        if not module:
            return Response({"message": "Module not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if all adaptive lessons in the module are completed
        is_completed = _module_completed(user, module.id)
        
        # We need the lesson IDs to fetch questions even if locked (for metadata) 
        # but normally we only fetch questions if unlocked.
        lesson_ids = _lesson_ids_for_user_module(user, module.id)
        
        if not is_completed:
            user_id = _progress_user_id(user)
            completed_count = UserProgress.objects.filter(
                user_id=user_id,
                lesson_id__in=lesson_ids,
                completed=True,
            ).count()
            
            return Response({
                "id": f"module-quiz-{module.id}",
                "title": f"{module.title} Comprehensive Quiz",
                "locked": True,
                "completedLessons": completed_count,
                "totalLessons": len(lesson_ids),
                "questions": []
            })

        # If unlocked, aggregate questions from ALL module lessons
        # Each lesson usually has a quiz. Find all quizzes for these lessons.
        import random
        
        lesson_questions = []
        for lid in lesson_ids:
            # Find quizzes for this specific lesson
            quizzes = Quiz.objects.filter(lesson_id=lid)
            lesson_qs_pool = list(Question.objects.filter(quiz_id__in=quizzes.values_list("id", flat=True)))
            if lesson_qs_pool:
                random.shuffle(lesson_qs_pool)
                # Take up to 3 questions from each lesson to ensure variety
                lesson_questions.extend(lesson_qs_pool[:3])
        
        # If we still have room, add more random questions from the module
        if len(lesson_questions) < 20:
            remaining_ids = Question.objects.filter(
                quiz_id__in=Quiz.objects.filter(lesson_id__in=lesson_ids).values_list("id", flat=True)
            ).exclude(id__in=[q.id for q in lesson_questions]).values_list("id", flat=True)
            
            extra_ids = random.sample(list(remaining_ids), min(len(remaining_ids), 20 - len(lesson_questions)))
            lesson_questions.extend(list(Question.objects.filter(id__in=extra_ids)))

        random.shuffle(lesson_questions)
        
        # Serialize and return
        final_questions = QuestionSerializer(lesson_questions[:30], many=True).data

        return Response({
            "id": f"module-quiz-{module.id}",
            "title": f"{module.title} Comprehensive Quiz",
            "locked": False,
            "questions": final_questions,
            "totalAvailable": Question.objects.filter(
                quiz_id__in=Quiz.objects.filter(lesson_id__in=lesson_ids)
            ).count()
        })
