import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from assessments.models import DiagnosticQuizAttempt

username = 'editionpython@gmail.com'
try:
    attempt = DiagnosticQuizAttempt.objects.filter(user__username=username).order_by('-created_at').first()
    if attempt:
        print(f"USER_REPORT_START")
        print(f"Username: {attempt.user.username}")
        print(f"Email: {attempt.user.email}")
        print(f"Overall Score: {attempt.overall_score:.1%}")
        print(f"Difficulty Tier: {attempt.difficulty_tier}")
        print(f"Completed At: {attempt.completed_at}")
        
        print("\nModule Breakdown:")
        for mod, score in attempt.module_scores.items():
            print(f"- {mod}: {score:.1%}")
        print(f"USER_REPORT_END")
    else:
        print(f"No attempt found for {username}")
except Exception as e:
    print(f"Error: {e}")
