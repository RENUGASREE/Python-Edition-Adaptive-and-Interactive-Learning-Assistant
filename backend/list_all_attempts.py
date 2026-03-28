import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import User
from assessments.models import DiagnosticQuizAttempt

print("All Diagnostic Quiz Attempts:")
attempts = DiagnosticQuizAttempt.objects.all().order_by('-created_at')
for attempt in attempts:
    print("-" * 50)
    print(f"User: {attempt.user.username} (ID: {attempt.user.id}, Email: {attempt.user.email})")
    print(f"Overall Score: {attempt.overall_score}")
    print(f"Difficulty Tier: {attempt.difficulty_tier}")
    print(f"Status: {attempt.status}")
    print(f"Module Scores: {json.dumps(attempt.module_scores, indent=2)}")
    print(f"Created At: {attempt.created_at}")
    print("-" * 50)

if not attempts.exists():
    print("No diagnostic quiz attempts found in the database.")
