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
        print(f"User: {attempt.user.username}")
        print(f"Overall Score: {attempt.overall_score}")
        print(f"Difficulty Tier: {attempt.difficulty_tier}")
        print("\nModule Scores:")
        for module, score in attempt.module_scores.items():
            status = "STRONG" if score >= 0.8 else ("IMPROVING" if score >= 0.5 else "WEAK")
            print(f" - {module}: {score * 100:.1f}% ({status})")
    else:
        print(f"No attempt found for {username}")
except Exception as e:
    print(f"Error: {e}")
