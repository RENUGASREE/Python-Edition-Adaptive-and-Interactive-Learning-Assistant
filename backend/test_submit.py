import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()
from django.utils import timezone
from core.models import User
from assessments.models import DiagnosticQuiz, DiagnosticQuizAttempt, DiagnosticQuestion
from assessments.services import score_diagnostic
from analytics.services.skill_analysis import analyze_user_skill_gaps

user = User.objects.get(email='editionpython@gmail.com')
quiz = DiagnosticQuiz.objects.order_by("-id").first()
attempt = DiagnosticQuizAttempt.objects.create(user=user, quiz=quiz, status="IN_PROGRESS", start_time=timezone.now())

violation_count = 0
questions = DiagnosticQuestion.objects.filter(quiz=quiz)
try:
    import json
    answers = []
    for q in questions:
        opts = q.options if isinstance(q.options, list) else json.loads(q.options)
        correct_opt = next((opt for opt in opts if opt.get("is_correct")), None)
        answers.append({"questionId": q.id, "selectedOptionId": correct_opt["id"] if correct_opt else None})
except Exception as e:
    import traceback
    with open("submit_trace.txt", "w", encoding="utf-8") as f:
        traceback.print_exc(file=f)
    print("Failed during answers build.")

module_scores, raw_score, weighted, tier = score_diagnostic(user, quiz.id, answers, violation_count=violation_count, update_user=True)
try:
    attempt.module_scores = module_scores
    attempt.overall_score = raw_score
    attempt.raw_score = raw_score
    attempt.weighted_score = weighted
    attempt.difficulty_tier = tier
    attempt.completed_at = timezone.now()
    attempt.locked = True
    attempt.status = "COMPLETED"
    attempt.save(update_fields=["module_scores", "overall_score", "raw_score", "weighted_score", "difficulty_tier", "completed_at", "locked", "status", "violation_count"])
    print("Attempt saved.")
except Exception as e:
    import traceback
    traceback.print_exc()

try:
    analyze_user_skill_gaps(user)
    print("Skill gaps analyzed.")
except Exception as e:
    import traceback
    traceback.print_exc()

print("Script completed.")
