import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import User
from assessments.models import DiagnosticQuizAttempt

def fetch_details(user_obj):
    attempt = DiagnosticQuizAttempt.objects.filter(user=user_obj).order_by('-created_at').first()
    if attempt:
        print(f"\nUser: {user_obj.username}")
        print(f"Overall Score: {attempt.overall_score:.3f} ({attempt.overall_score * 100:.1f}%)")
        print(f"Difficulty Tier: {attempt.difficulty_tier}")
        print("Module Scores:")
        for module, score in attempt.module_scores.items():
            status = "STRONG" if score >= 0.8 else ("IMPROVING" if score >= 0.5 else "WEAK")
            print(f" - {module}: {score * 100:.1f}% ({status})")
    else:
        print(f"No placement quiz attempt found for user: {user_obj.username}")

# Check exact match
try:
    user_python = User.objects.get(username='Python')
    fetch_details(user_python)
except User.DoesNotExist:
    # Check case-insensitive match
    try:
        user_python = User.objects.get(username__iexact='Python')
        fetch_details(user_python)
    except User.DoesNotExist:
        # Check email match
        try:
            user_python = User.objects.get(email='editionpython@gmail.com')
            fetch_details(user_python)
        except User.DoesNotExist:
             print("User 'Python' or 'editionpython@gmail.com' not found.")
