"""Django management command to fully reset a user's progress."""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import UserProgress, UserMastery
from assessments.models import DiagnosticQuizAttempt


class Command(BaseCommand):
    help = 'Fully reset progress and diagnostic data for a user by username'

    def add_arguments(self, parser):
        parser.add_argument('usernames', nargs='+', type=str, help='Usernames to reset')

    def handle(self, *args, **options):
        User = get_user_model()

        for username in options['usernames']:
            try:
                u = User.objects.get(username__iexact=username)
                self.stdout.write(f"\nResetting user: {u.username} (id={u.id}, uuid={u.original_uuid})")

                # Delete UserProgress by every possible user_id format
                ids_to_try = set()
                ids_to_try.add(str(u.id))
                if u.original_uuid:
                    ids_to_try.add(str(u.original_uuid))

                total_progress = 0
                for uid in ids_to_try:
                    d = UserProgress.objects.filter(user_id=uid).delete()
                    total_progress += d[0]
                    if d[0]:
                        self.stdout.write(f"  Deleted {d[0]} progress records for user_id={uid}")

                # Also try FK-based deletion if supported
                try:
                    d = UserProgress.objects.filter(user=u).delete()
                    total_progress += d[0]
                    if d[0]:
                        self.stdout.write(f"  Deleted {d[0]} progress records via user FK")
                except Exception:
                    pass

                # Delete diagnostic attempts
                d = DiagnosticQuizAttempt.objects.filter(user=u).delete()
                self.stdout.write(f"  Deleted {d[0]} diagnostic attempts")

                # Delete mastery records
                d = UserMastery.objects.filter(user=u).delete()
                self.stdout.write(f"  Deleted {d[0]} mastery records")

                # Reset user flags
                u.has_taken_quiz = False
                u.diagnostic_completed = False
                u.mastery_vector = {}
                u.level = 'Beginner'
                u.save(update_fields=['has_taken_quiz', 'diagnostic_completed', 'mastery_vector', 'level'])

                self.stdout.write(self.style.SUCCESS(
                    f"  DONE: {username} fully reset | {total_progress} progress records deleted"
                ))

            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"User not found: {username}"))
