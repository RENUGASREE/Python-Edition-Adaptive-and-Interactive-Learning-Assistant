from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection
from core.models import Progress, QuizAttempt, Certificate, Recommendation, ChatMessage, UserMastery
from gamification.models import UserBadge, XpEvent, Streak
from evaluation.models import RecommendationEvent, RecommendationOutcome, RecommendationStrategyAssignment
from recommendation.models import UserTopicBehavior, DifficultyShift

class Command(BaseCommand):
    help = "Delete all users"

    def handle(self, *args, **options):
        User = get_user_model()
        try:
            RecommendationOutcome.objects.all().delete()
        except Exception:
            pass
        try:
            RecommendationEvent.objects.all().delete()
        except Exception:
            pass
        try:
            RecommendationStrategyAssignment.objects.all().delete()
        except Exception:
            pass
        try:
            UserBadge.objects.all().delete()
        except Exception:
            pass
        try:
            XpEvent.objects.all().delete()
        except Exception:
            pass
        try:
            Streak.objects.all().delete()
        except Exception:
            pass
        try:
            Progress.objects.all().delete()
        except Exception:
            pass
        try:
            QuizAttempt.objects.all().delete()
        except Exception:
            pass
        try:
            Certificate.objects.all().delete()
        except Exception:
            pass
        try:
            Recommendation.objects.all().delete()
        except Exception:
            pass
        try:
            ChatMessage.objects.all().delete()
        except Exception:
            pass
        try:
            UserMastery.objects.all().delete()
        except Exception:
            pass

        try:
            UserTopicBehavior.objects.all().delete()
        except Exception:
            pass
        try:
            DifficultyShift.objects.all().delete()
        except Exception:
            pass
        with connection.cursor() as cursor:
            try:
                cursor.execute('DELETE FROM "django_admin_log"')
            except Exception:
                pass
        table = User._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute(f'DELETE FROM "{table}"')
        self.stdout.write(self.style.SUCCESS("All users deleted"))
