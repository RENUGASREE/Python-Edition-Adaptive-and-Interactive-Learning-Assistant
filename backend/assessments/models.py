from django.db import models
from core.models import User


class DiagnosticQuiz(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class DiagnosticQuestion(models.Model):
    quiz = models.ForeignKey(DiagnosticQuiz, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=50)
    text = models.TextField()
    options = models.JSONField(blank=True, null=True)
    correct_index = models.IntegerField()
    points = models.IntegerField(default=1)

class DiagnosticOption(models.Model):
    question = models.ForeignKey(DiagnosticQuestion, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)


class DiagnosticQuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(DiagnosticQuiz, on_delete=models.CASCADE)
    module_scores = models.JSONField(default=dict)
    overall_score = models.FloatField(default=0)
    difficulty_tier = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.IntegerField(default=900)
    completed_at = models.DateTimeField(null=True, blank=True)
    violation_count = models.IntegerField(default=0)
    raw_score = models.FloatField(default=0)
    weighted_score = models.FloatField(default=0)
    locked = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        default="NOT_STARTED",
        choices=[
            ("NOT_STARTED", "NOT_STARTED"),
            ("IN_PROGRESS", "IN_PROGRESS"),
            ("COMPLETED", "COMPLETED"),
            ("CANCELLED", "CANCELLED"),
            ("INVALID", "INVALID"),
        ],
    )


class AssessmentInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    correctness = models.BooleanField()
    time_spent = models.FloatField(default=0)
    hints_used = models.IntegerField(default=0)
    source = models.CharField(max_length=50, default="quiz")
    created_at = models.DateTimeField(auto_now_add=True)
