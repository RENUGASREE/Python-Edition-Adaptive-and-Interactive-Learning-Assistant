from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, UserProfileView, LogoutView, RunChallengeView, ProgressViewSet, QuizAttemptViewSet, BadgeViewSet, CertificateViewSet, RecommendationViewSet, ChatMessageViewSet, ModuleViewSet, LessonViewSet, UserProgressViewSet, QuizViewSet, QuestionViewSet, ChallengeViewSet, MasteryUpdateView, AdaptiveRecommendationView, SubmitQuizView

router = DefaultRouter()
router.register(r'modules', ModuleViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'quizzes', QuizViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'challenges', ChallengeViewSet)
router.register(r'user-progress', UserProgressViewSet) # New endpoint matching Node behavior?
router.register(r'progress', ProgressViewSet)
router.register(r'quiz-attempts', QuizAttemptViewSet)
router.register(r'badges', BadgeViewSet)
router.register(r'certificates', CertificateViewSet)
router.register(r'recommendations', RecommendationViewSet)
router.register(r'chatmessages', ChatMessageViewSet)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/user/', UserProfileView.as_view(), name='user_profile'),
    path('auth/user/update/', UserProfileView.as_view(), name='user_profile_update'),  # New endpoint for updates
    path('auth/user/avatar/', UserProfileView.as_view(), name='user_avatar'),  # Avatar upload endpoint
    path('logout/', LogoutView.as_view(), name='logout'),
    path('mastery/update/', MasteryUpdateView.as_view(), name='mastery_update'),
    path('recommendations/next/', AdaptiveRecommendationView.as_view(), name='recommendations_next'),
    path('challenges/<int:id>/run/', RunChallengeView.as_view(), name='run_challenge'),
    path('quizzes/<int:quiz_id>/submit/', SubmitQuizView.as_view(), name='submit_quiz'),
    path('', include(router.urls)),
]
