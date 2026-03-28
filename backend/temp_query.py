import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adaptive_learning.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import DiagnosticAttempt, UserMastery, QuizAttempt

User = get_user_model()
try:
    user = User.objects.get(username="Python")
    print("User found:", user.username)
    print("Level:", user.level)
    print("Engagement Score:", user.engagement_score)
    print("Diagnostic Completed:", user.diagnostic_completed)
    print("Mastery Vector:", user.mastery_vector)
    
    attempts = DiagnosticAttempt.objects.filter(user=user).order_by('-created_at')
    print("\nDiagnostic Attempts (Placement Quiz):", attempts.count())
    for attempt in attempts:
        print(f"- Date: {attempt.created_at}, Overall Score: {attempt.overall_score}, Module Scores: {attempt.module_scores}")
        
    masteries = UserMastery.objects.filter(user=user)
    print("\nUser Mastery:")
    for m in masteries:
        print(f"- Module: {m.module_id}, Score: {m.mastery_score}, Last Source: {m.last_source}")
        
    quiz_attempts = QuizAttempt.objects.filter(user=user)
    print("\nOther Quiz Attempts:")
    for qa in quiz_attempts:
        print(f"- Quiz ID: {qa.quiz.id if qa.quiz else 'None'}, Score: {qa.score}/{qa.total_questions}, Notes: {qa.notes}")
        
except User.DoesNotExist:
    print("User 'Python' not found.")
except Exception as e:
    print(f"Error: {e}")
