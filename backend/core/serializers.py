import re
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import User, Progress, QuizAttempt, Badge, Certificate, Recommendation, ChatMessage, Module, Lesson, Quiz, Question, Challenge, UserProgress, UserMastery, DiagnosticAttempt, DiagnosticQuestionMeta
from lessons.models import LessonProfile
from django.db.models import Sum
from datetime import timedelta
from django.utils import timezone
from gamification.models import XpEvent, Streak
from recommendation.services import normalize_topic

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    firstName = serializers.CharField(source='first_name', required=False, allow_blank=True)
    lastName = serializers.CharField(source='last_name', required=False, allow_blank=True)
    masteryVector = serializers.JSONField(source='mastery_vector', required=False)
    stats = serializers.SerializerMethodField()
    achievements = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(source='date_joined', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'firstName', 'lastName', 'level', 'masteryVector', 'engagement_score', 'diagnostic_completed', 'has_taken_quiz', 'learning_velocity', 'stats', 'achievements', 'createdAt')
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': False} # Fallback handled in create
        }

    def get_stats(self, obj):
        # Get user progress
        # Check if using integer ID or UUID string
        user_key = obj.original_uuid or str(obj.id)
        all_completed_qs = UserProgress.objects.filter(user_id=user_key, completed=True)
        completed_lessons = all_completed_qs.count()

        # Weekly progress: lessons completed in the last 7 days
        now = timezone.now()
        week_ago = now - timedelta(days=7)
        weekly_completed = all_completed_qs.filter(
            completed_at__isnull=False,
            completed_at__gte=week_ago,
        ).count()
        weekly_goal = 5
        weekly_progress = min(weekly_completed, weekly_goal)

        total_points = XpEvent.objects.filter(user=obj).aggregate(total_points=Sum("points")).get("total_points") or 0
        
        streak_obj = Streak.objects.filter(user=obj).first()
        streak = streak_obj.current_streak if streak_obj else 0

        return {
            'completedLessons': completed_lessons,
            'totalPoints': total_points,
            'streak': streak,
            'weeklyGoal': weekly_goal,
            'weeklyProgress': weekly_progress
        }

    def get_achievements(self, obj):
        if obj.original_uuid:
            progress_qs = UserProgress.objects.filter(user_id=obj.original_uuid, completed=True)
        else:
            progress_qs = UserProgress.objects.filter(user_id=str(obj.id), completed=True)
            
        completed_lessons = progress_qs.count()
        streak_obj = Streak.objects.filter(user=obj).first()
        current_streak = streak_obj.current_streak if streak_obj else 0
        xp_total = XpEvent.objects.filter(user=obj).aggregate(total_points=Sum("points")).get("total_points") or 0

        modules = Module.objects.all()
        module_completed = False
        for module in modules:
            lesson_ids = list(Lesson.objects.filter(module_id=module.id).values_list("id", flat=True))
            if not lesson_ids:
                continue
            completed_count = UserProgress.objects.filter(
                user_id=obj.original_uuid or str(obj.id),
                lesson_id__in=lesson_ids,
                completed=True,
            ).count()
            if completed_count == len(lesson_ids):
                module_completed = True
                break

        achievements_list = []
        if completed_lessons >= 1:
            achievements_list.append({
                "id": "1",
                "title": "First Steps",
                "description": "Complete your first lesson",
                "icon": "Star",
                "progress": 1,
                "maxProgress": 1,
                "unlocked": True,
                "points": 10,
                "category": "Beginner"
            })
        if completed_lessons >= 10:
            achievements_list.append({
                "id": "2",
                "title": "Code Warrior",
                "description": "Complete 10 lessons",
                "icon": "Target",
                "progress": 10,
                "maxProgress": 10,
                "unlocked": True,
                "points": 50,
                "category": "Challenges"
            })
        if current_streak >= 7:
            achievements_list.append({
                "id": "3",
                "title": "Streak Master",
                "description": "Maintain a 7-day learning streak",
                "icon": "Zap",
                "progress": 7,
                "maxProgress": 7,
                "unlocked": True,
                "points": 100,
                "category": "Consistency"
            })
        if module_completed:
            achievements_list.append({
                "id": "4",
                "title": "Module Champion",
                "description": "Complete an entire module",
                "icon": "Award",
                "progress": 1,
                "maxProgress": 1,
                "unlocked": True,
                "points": 75,
                "category": "Progress"
            })
        if completed_lessons >= 25:
            achievements_list.append({
                "id": "5",
                "title": "Python Expert",
                "description": "Complete all Python lessons",
                "icon": "Crown",
                "progress": 25,
                "maxProgress": 25,
                "unlocked": True,
                "points": 200,
                "category": "Mastery"
            })

        return achievements_list

    def create(self, validated_data):
        # Prioritize explicit username, then email, then generate one if both missing
        username = validated_data.get('username')
        email = validated_data.get('email')
        
        # Ensure we use the provided username if it exists and is not just whitespace
        if not username or (isinstance(username, str) and not username.strip()):
            username = email or f"user_{int(timezone.now().timestamp())}"
            
        # Explicit initialization of adaptive fields for a clean new-user state
        user = User(
            username=username,
            email=email or "",
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            level="Beginner",
            diagnostic_completed=False,
            has_taken_quiz=False,
            mastery_vector={}
        )
        try:
            validate_password(validated_data['password'], user)
        except DjangoValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_email(self, value):
        instance = getattr(self, 'instance', None)
        if instance and instance.email == value:
            return value
        qs = User.objects.filter(email=value)
        if instance:
            qs = qs.exclude(id=instance.id)
        if qs.exists():
            raise serializers.ValidationError("This email address is already in use.")
        return value

# --- Content Serializers ---

class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    quizId = serializers.CharField(source='quiz_id')

    class Meta:
        model = Question
        fields = ('id', 'quizId', 'text', 'type', 'options', 'points')

    def to_representation(self, instance):
        import random
        ret = super().to_representation(instance)
        options = ret.get('options')
        if isinstance(options, list):
            # Create a copy and shuffle it
            shuffled_options = list(options)
            random.shuffle(shuffled_options)
            ret['options'] = shuffled_options
        return ret

class QuizSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    lessonId = serializers.CharField(source='lesson_id')
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ('id', 'lessonId', 'title', 'questions')

    def get_questions(self, obj):
        questions = Question.objects.filter(quiz_id=obj.id)
        return QuestionSerializer(questions, many=True).data

class ChallengeSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    lessonId = serializers.CharField(source='lesson_id')
    initialCode = serializers.CharField(source='initial_code')
    solutionCode = serializers.CharField(source='solution_code', required=False)
    testCases = serializers.JSONField(source='test_cases')

    class Meta:
        model = Challenge
        fields = ('id', 'lessonId', 'title', 'description', 'initialCode', 'solutionCode', 'testCases', 'points', 'difficulty')

# Forward declaration or separate serializer to avoid circular dependency
class SimpleModuleSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    imageUrl = serializers.CharField(source='image_url', required=False)
    
    class Meta:
        model = Module
        fields = ('id', 'title', 'description', 'order', 'imageUrl')

class LessonSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    moduleId = serializers.CharField(source='module_id')
    quizzes = serializers.SerializerMethodField()
    challenges = serializers.SerializerMethodField()
    module = serializers.SerializerMethodField() 
    unlocked = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()

    nextLessonId = serializers.SerializerMethodField()
    previousLessonId = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('id', 'moduleId', 'title', 'slug', 'content', 'order', 'difficulty', 'duration', 'quizzes', 'challenges', 'module', 'unlocked', 'completed', 'nextLessonId', 'previousLessonId')

    def get_unlocked(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        # Import here to avoid circular dependencies if any
        from .views import _lesson_unlocked
        return _lesson_unlocked(request.user, obj)

    def get_completed(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        from .views import _progress_user_id, UserProgress
        user_id = _progress_user_id(request.user)
        return UserProgress.objects.filter(user_id=user_id, lesson_id=obj.id, completed=True).exists()

    def get_nextLessonId(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return None
        from .views import _lesson_ids_for_user_module
        allowed_ids = _lesson_ids_for_user_module(request.user, obj.module_id)
        # ordered_lessons = list(Lesson.objects.filter(id__in=allowed_ids).order_by("order", "id"))
        # Using a list comprehension to preserve order from allowed_ids if it's already sorted
        # but _lesson_ids_for_user_module might not guarantee 'order' field sorting.
        # Actually, let's just use the IDs in sequence as determined by the adaptive logic.
        try:
            curr_idx = allowed_ids.index(obj.id)
            if curr_idx < len(allowed_ids) - 1:
                return allowed_ids[curr_idx + 1]
        except (ValueError, IndexError):
            pass
        return None

    def get_previousLessonId(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return None
        from .views import _lesson_ids_for_user_module
        allowed_ids = _lesson_ids_for_user_module(request.user, obj.module_id)
        try:
            curr_idx = allowed_ids.index(obj.id)
            if curr_idx > 0:
                return allowed_ids[curr_idx - 1]
        except (ValueError, IndexError):
            pass
        return None

    def get_quizzes(self, obj):
        request = self.context.get("request")
        user = request.user if request and request.user.is_authenticated else None
        
        quizzes = Quiz.objects.filter(lesson_id=obj.id)
        if not quizzes.exists():
            # Fallback: Return a dynamic quiz if none exists in DB
            from .services.ai_quiz_generator import generate_quiz_from_lesson
            dynamic_questions = generate_quiz_from_lesson(obj)
            return [{
                "id": f"dynamic-quiz-{obj.id}", # String ID for fallback
                "title": f"Lesson Checkpoint: {obj.title}",
                "questions": [
                    {
                        "id": f"dynamic-ques-{obj.id}-{idx}", # String ID for fallback
                        "text": q["question"],
                        "options": [
                            {
                                "id": i,
                                "text": opt,
                                "correct": i == q.get("correct", -1)
                            }
                            for i, opt in enumerate(q["options"])
                        ],
                        "correct_option_idx": q["correct"],
                        "points": 10
                    } for idx, q in enumerate(dynamic_questions)
                ],
                "attempted": False,
                "score": None,
                "total_questions": len(dynamic_questions),
            }]

        quiz_data = []
        for quiz in quizzes:
            attempt = None
            if user:
                attempt = QuizAttempt.objects.filter(user=user, quiz=quiz).first()
            
            questions = Question.objects.filter(quiz_id=quiz.id)
            quiz_data.append({
                "id": quiz.id,
                "title": quiz.title,
                "questions": QuestionSerializer(questions, many=True).data,
                "attempted": attempt is not None,
                "score": attempt.score if attempt else None,
                "total_questions": attempt.total_questions if attempt else None,
            })
        return quiz_data

    def get_challenges(self, obj):
        challenges = Challenge.objects.filter(lesson_id=obj.id)
        return ChallengeSerializer(challenges, many=True).data
    
    def get_module(self, obj):
        module = Module.objects.filter(id=obj.module_id).first()
        return SimpleModuleSerializer(module).data if module else None

class SimpleLessonSerializer(serializers.ModelSerializer):
    moduleId = serializers.CharField(source='module_id')
    topic = serializers.SerializerMethodField()
    prerequisites = serializers.SerializerMethodField()
    embeddingVector = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('id', 'moduleId', 'title', 'slug', 'content', 'order', 'difficulty', 'duration', 'topic', 'prerequisites', 'embeddingVector')

    def _profile(self, obj):
        return LessonProfile.objects.filter(lesson_id=obj.id).first()

    def get_topic(self, obj):
        profile = self._profile(obj)
        return normalize_topic(profile.topic) if profile else None

    def get_prerequisites(self, obj):
        profile = self._profile(obj)
        return profile.prerequisites if profile else []

    def get_embeddingVector(self, obj):
        profile = self._profile(obj)
        return profile.embedding_vector if profile else []

class ModuleSerializer(serializers.ModelSerializer):
    imageUrl = serializers.CharField(source='image_url', required=False)
    lessons = serializers.SerializerMethodField()
    quizLocked = serializers.SerializerMethodField()
    quizCompleted = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ('id', 'title', 'description', 'order', 'imageUrl', 'lessons', 'quizLocked', 'quizCompleted')

    def get_quizLocked(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return True
        from .views import _module_completed
        return not _module_completed(request.user, obj.id)

    def get_quizCompleted(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        # Check if any quiz attempt exists for this module
        # Attempts currently store "module:{id}:level:{level}" in notes
        from .models import QuizAttempt
        return QuizAttempt.objects.filter(
            user=request.user, 
            notes__icontains=f"module:{obj.id}:level:"
        ).exists()

    def get_lessons(self, obj):
        # ... (keep existing implementation)
        request = self.context.get("request")
        user = request.user if request else None
        if not user or not user.is_authenticated:
            return []
        
        # Step 1: Check pre-calculated context (Performance Optimization)
        # This prevents redundant database scans for each module in the list
        precalculated = self.context.get("precalculated_difficulties", {})
        
        assigned_difficulty = None
        # Support both dashed and underscored module IDs for robustness
        mod_id = str(obj.id)
        search_keys = [mod_id, mod_id.replace("-", "_")]
        
        # Special case mappings from diagnostic quiz keys to module IDs
        special_mappings = {
            "mod-python-basics": ["mod_introduction", "mod-introduction"],
            "mod-data-types": ["mod_variables_types", "mod-variables-types"],
            "mod-control-flow": ["mod_control_flow", "mod_loops_iteration", "mod-loops-iteration"],
            "mod-functions": ["mod_functions_scope", "mod-functions-scope"],
            "mod-modules-packages": ["mod_file_handling", "mod-error-handling", "mod-file-handling", "mod-error-handling"],
        }
        if mod_id in special_mappings:
            search_keys.extend(special_mappings[mod_id])
            
        for sk in search_keys:
            # Support both original case and lowercase matching for maximum robustness
            if sk in precalculated:
                assigned_difficulty = precalculated[sk]
                break
            if sk.lower() in precalculated:
                assigned_difficulty = precalculated[sk.lower()]
                break
        
        if not assigned_difficulty:
            # Step 2: Fallback to old mastery_vector check (safety mechanism)
            mastery_vector = user.mastery_vector or {}
            difficulty_map = mastery_vector.get("_module_difficulty", {})
            for sk in search_keys:
                if sk in difficulty_map:
                    assigned_difficulty = difficulty_map[sk]
                    break
        
        if not assigned_difficulty:
            # Step 3: Final fallback to legacy quiz attempt logs
            from .models import QuizAttempt as CoreQuizAttempt
            attempts = CoreQuizAttempt.objects.filter(user=user).order_by("completed_at")
            for attempt in attempts:
                notes = attempt.notes or ""
                # Support both numeric and slug-based module IDs (e.g., mod-python-basics)
                match = re.search(r"module:([\w-]+):level:([A-Za-z]+)", notes)
                if match and match.group(1).lower() == str(obj.id).lower():
                    assigned_difficulty = match.group(2)
        
        target_level = assigned_difficulty or user.level or "Beginner"
        normalized = target_level.strip().lower()
        if normalized in ("pro", "advanced"):
            normalized = "Pro"  # Database uses "Pro"
        elif normalized == "intermediate":
            normalized = "Intermediate"
        else:
            normalized = "Beginner"
            
        lessons = list(Lesson.objects.filter(module_id=obj.id, difficulty=normalized).order_by('order'))
        if not lessons:
            lessons = list(Lesson.objects.filter(module_id=obj.id).order_by('order'))
            
        user_id = user.original_uuid or str(user.id)
        completed_ids = set(UserProgress.objects.filter(
            user_id=user_id,
            lesson_id__in=[lesson.id for lesson in lessons],
            completed=True,
        ).values_list("lesson_id", flat=True))
        
        prereq_map = {
            item["lesson_id"]: (item["prerequisites"] or [])
            for item in LessonProfile.objects.filter(lesson_id__in=[lesson.id for lesson in lessons]).values("lesson_id", "prerequisites")
        }
        
        unlocked = []
        for idx, lesson in enumerate(lessons):
            from .views import _lesson_unlocked
            is_unlocked = _lesson_unlocked(user, lesson)
            
            # Use SimpleLessonSerializer if LessonSerializer causes circular issues
            data = LessonSerializer(lesson, context=self.context).data
            data["unlocked"] = is_unlocked
            data["completed"] = lesson.id in completed_ids
            unlocked.append(data)
        return unlocked

# --- End Content Serializers ---

class UserProgressSerializer(serializers.ModelSerializer):
    userId = serializers.CharField(source='user_id', read_only=False)
    lessonId = serializers.CharField(source='lesson_id')
    lastCode = serializers.CharField(source='last_code', required=False, allow_blank=True)
    completedAt = serializers.DateTimeField(source='completed_at', required=False, allow_null=True)

    quizCompleted = serializers.BooleanField(source='quiz_completed', required=False, allow_null=True)
    challengeCompleted = serializers.BooleanField(source='challenge_completed', required=False, allow_null=True)

    class Meta:
        model = UserProgress
        fields = ('id', 'userId', 'lessonId', 'completed', 'quizCompleted', 'challengeCompleted', 'score', 'lastCode', 'completedAt')
    
    def create(self, validated_data):
        # Remove userId if present and use the one from the request
        return super().create(validated_data)

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = '__all__'

class UserMasterySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMastery
        fields = '__all__'

class DiagnosticAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosticAttempt
        fields = '__all__'

class DiagnosticQuestionMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosticQuestionMeta
        fields = '__all__'

class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = '__all__'


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = '__all__'


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'
