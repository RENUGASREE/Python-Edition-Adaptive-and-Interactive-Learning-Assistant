import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from assessments.models import DiagnosticQuizAttempt

username = 'editionpython@gmail.com'
try:
    attempt = DiagnosticQuizAttempt.objects.filter(user__username=username).order_by('-created_at').first()
    if attempt:
        # Avoid non-ascii or encoding issues by printing very simply
        data = {
            "user": attempt.user.username,
            "overall": attempt.overall_score,
            "tier": attempt.difficulty_tier,
            "scores": attempt.module_scores
        }
        print(json.dumps(data, indent=2))
    else:
        print(f"No attempt found for {username}")
except Exception as e:
    print(f"Error: {e}")
