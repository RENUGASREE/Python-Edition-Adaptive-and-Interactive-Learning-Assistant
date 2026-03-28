import os
import django
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import User
from assessments.models import DiagnosticQuizAttempt

def get_user_performance(username):
    try:
        user = User.objects.get(username=username)
        print(f"User found: {user.username} (ID: {user.id})")
        
        attempts = DiagnosticQuizAttempt.objects.filter(user=user).order_by('-created_at')
        if not attempts.exists():
            print(f"No diagnostic quiz attempts found for user '{username}'.")
            return
        
        print(f"Found {attempts.count()} attempt(s).")
        for i, attempt in enumerate(attempts):
            print(f"\n--- Attempt {i+1} ({attempt.created_at}) ---")
            print(f"Status: {attempt.status}")
            print(f"Overall Score: {attempt.overall_score}")
            print(f"Difficulty Tier: {attempt.difficulty_tier}")
            print(f"Module Scores: {json.dumps(attempt.module_scores, indent=2)}")
            print(f"Raw Score: {attempt.raw_score}")
            print(f"Weighted Score: {attempt.weighted_score}")
            print(f"Completion Time: {attempt.completed_at}")
            
    except User.DoesNotExist:
        print(f"User '{username}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_user_performance("Python")
