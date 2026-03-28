import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import User
from assessments.models import DiagnosticQuizAttempt

username = 'editionpython@gmail.com'
try:
    user = User.objects.get(username=username)
    attempts = DiagnosticQuizAttempt.objects.filter(user=user).order_by('-created_at')
    
    if attempts.exists():
        attempt = attempts[0]
        performance = {
            "username": user.username,
            "overall_score": attempt.overall_score,
            "difficulty_tier": attempt.difficulty_tier,
            "status": attempt.status,
            "module_scores": attempt.module_scores,
            "raw_score": attempt.raw_score,
            "weighted_score": attempt.weighted_score,
            "completed_at": str(attempt.completed_at)
        }
        print(json.dumps(performance, indent=4))
    else:
        print(f"No attempts found for {username}")
except User.DoesNotExist:
    print(f"User {username} not found")
