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
import openai
import os

logger = logging.getLogger(__name__)

def normalize_level_for_score(score):
    if score < 50:
        return "Beginner"
    if score < 75:
        return "Intermediate"
    return "Advanced"

def map_level_to_db(level):
    if not level:
        return "Beginner"
    lower = level.strip().lower()
    if lower in ["advanced", "pro"]:
        return "Pro"
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
    if topic:
        mastery_vector[topic] = new_score
    else:
        mastery_vector[str(module_id)] = new_score
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
    # QuizAttempt uses `completed_at` as the timestamp field.
    # Ordering by a non-existent field can raise FieldError and break `/api/modules/`.
    attempts = QuizAttempt.objects.filter(user=user).order_by("completed_at")
    for attempt in attempts:
        match = re.search(r"module:(\d+):level:([A-Za-z]+)", attempt.notes or "")
        if match:
            levels[int(match.group(1))] = match.group(2)
    return levels

def _normalize_level(level):
    if not level:
        return "Beginner"
    lower = level.strip().lower()
    if lower == "advanced":
        return "Pro"
    if lower == "intermediate":
        return "Intermediate"
    return "Beginner"

def _lesson_ids_for_user_module(user, module_id):
    level_map = _module_level_map(user)
    target_level = _normalize_level(level_map.get(module_id) or user.level or "Beginner")
    lesson_ids = list(Lesson.objects.filter(module_id=module_id, difficulty=target_level).values_list("id", flat=True))
    if lesson_ids:
        return lesson_ids
    return list(Lesson.objects.filter(module_id=module_id).values_list("id", flat=True))

def _prerequisites_met(user, lesson_id: int) -> bool:
    profile = LessonProfile.objects.filter(lesson_id=int(lesson_id)).first()
    prereqs = list((profile.prerequisites or []) if profile else [])
    if not prereqs:
        return True
    try:
        prereq_ids = [int(val) for val in prereqs]
    except Exception:
        prereq_ids = []
        for val in prereqs:
            try:
                prereq_ids.append(int(val))
            except Exception:
                continue
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

    allowed_ids = _lesson_ids_for_user_module(user, lesson.module_id)
    ordered_lessons = list(Lesson.objects.filter(id__in=allowed_ids).order_by("order"))
    # Find the immediate previous lesson in the ordered list
    previous_lesson = next((item for item in reversed(ordered_lessons) if item.order < lesson.order), None)
    
    if not previous_lesson:
        return _prerequisites_met(user, lesson.id)
        
    user_id = _progress_user_id(user)
    sequential_ok = UserProgress.objects.filter(
        user_id=user_id,
        lesson_id=previous_lesson.id,
        completed=True,
    ).exists()
    
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
                error_messages.append("Registration failed due to invalid data.")
            return Response({'message': '; '.join(error_messages)}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        # login(request, user) # Removed to avoid session/CSRF issues with JWT
        
        # Generate JWT tokens for immediate login
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

    def post(self, request, id):
        code = request.data.get('code', '')
        if not code.strip():
            return Response({'message': 'Please write some code before running.'}, status=status.HTTP_400_BAD_REQUEST)

        def run_code(code_to_run):
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

            if test_cases:
                for tc in test_cases:
                    tc_input = str(tc.get("input") or "")
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
                        combined_output += out + ("\n" if out else "")
                        expected = str(tc.get("expected", "")).strip()
                        if err or out != expected:
                            all_passed = False
                            if err:
                                error_message = err
                            else:
                                error_message = f"Expected '{expected}', got '{out}'"
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
                stdout, stderr = run_code(code)
                combined_output = stdout
                if stderr:
                    all_passed = False
                    error_message = stderr
                elif challenge.solution_code:
                    expected_stdout, expected_stderr = run_code(challenge.solution_code)
                    if expected_stderr:
                        all_passed = False
                        error_message = "Reference solution failed to run"
                    else:
                        all_passed = stdout.strip() == expected_stdout.strip()
                        if not all_passed:
                            error_message = "Output does not match the expected result"

            if challenge and challenge.lesson_id:
                lesson = Lesson.objects.filter(id=challenge.lesson_id).first()
                if lesson:
                    topic = LessonProfile.objects.filter(lesson_id=lesson.id).values_list("topic", flat=True).first() or lesson.title
                    log_assessment_interaction(request.user, topic, all_passed, 0, 0, "challenge")
                    update_engagement(request.user, 0.01 if all_passed else -0.01)
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
        if not _quiz_completed(request.user):
            return Response({"message": "You need to complete the placement quiz to personalize your learning path."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user_id = user.original_uuid or str(user.id)
        lesson_id = serializer.validated_data.get("lesson_id")
        completed = serializer.validated_data.get("completed")
        score = serializer.validated_data.get("score")
        last_code = serializer.validated_data.get("last_code")
        completed_at = serializer.validated_data.get("completed_at")
        time_spent = request.data.get("timeSpent", 0)
        hints_used = request.data.get("hintsUsed", 0)
        if completed and not completed_at:
            completed_at = timezone.now()

        progress, _ = UserProgress.objects.update_or_create(
            user_id=user_id,
            lesson_id=lesson_id,
            defaults={
                "completed": completed,
                "score": score,
                "last_code": last_code,
                "completed_at": completed_at,
            },
        )
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
                target_level = (lesson.difficulty or user.level or "Beginner").strip()
                if target_level.lower() == "advanced":
                    target_level = "Pro"
                lessons_in_module = Lesson.objects.filter(module_id=lesson.module_id, difficulty=target_level)
                if not lessons_in_module:
                    lessons_in_module = Lesson.objects.filter(module_id=lesson.module_id)
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
            question_id = answer.get("questionId")
            selected_index = answer.get("selectedIndex")
            if question_id is not None:
                answers_map[int(question_id)] = selected_index

        module_totals = {}
        module_correct = {}
        total_questions = 0
        correct_answers = 0

        for question in questions:
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
        topic = request.data.get("topic")
        correct = request.data.get("correct")
        time_spent = request.data.get("timeSpent", 0)
        hints_used = request.data.get("hintsUsed", 0)
        if topic is not None and correct is not None:
            log_assessment_interaction(request.user, topic, bool(correct), float(time_spent or 0), int(hints_used or 0), "quiz")
        analyze_user_skill_gaps(request.user)
        output = self.get_serializer(progress).data
        return Response(output, status=status.HTTP_200_OK)


class SubmitQuizView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, quiz_id):
        logger.info(f"User {request.user.id} submitting quiz {quiz_id}")
        try:
            quiz = Quiz.objects.get(id=quiz_id)
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

        return Response({
            "score": score,
            "total": total_questions,
            "percentage": round((score / total_questions) * 100, 2) if total_questions > 0 else 0
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
        try:
            certificate = Certificate.objects.get(user=user, module_id=module_id)
        except Certificate.DoesNotExist:
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
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        query = request.data.get('query')
        if not query:
            return Response({'error': 'Query not provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "YOUR_API_KEY"))

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful Python tutor."},
                    {"role": "user", "content": query}
                ]
            )

            response_data = {
                'response': response.choices[0].message.content,
                'source_topic': 'General',
                'confidence_score': 0.99
            }
            return Response(response_data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
