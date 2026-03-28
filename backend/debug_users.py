import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import User

print("Full User List:")
for user in User.objects.all():
    print(f"ID: {user.id} | Username: {repr(user.username)} | Email: {repr(user.email)}")

from assessments.models import DiagnosticQuizAttempt
print("\nUsers with diagnostic quiz attempts:")
for attempt in DiagnosticQuizAttempt.objects.all():
    print(f"User: {attempt.user.username} (ID: {attempt.user.id}) | Score: {attempt.overall_score} | Tier: {attempt.difficulty_tier}")
