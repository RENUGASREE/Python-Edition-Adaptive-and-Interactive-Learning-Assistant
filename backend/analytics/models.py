from django.db import models
from core.models import User


class SkillGapAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="skill_gaps")
    topic = models.CharField(max_length=255, db_index=True)
    accuracy = models.FloatField(default=0.0)
    status = models.CharField(max_length=20)  # WEAK / IMPROVING / STRONG
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "topic")
        indexes = [
            models.Index(fields=["user", "topic"]),
            models.Index(fields=["user", "status"]),
        ]


class LearningPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="learning_plans")
    generated_at = models.DateTimeField(auto_now_add=True)
    recommended_modules = models.JSONField(default=list, blank=True)
    recommended_lessons = models.JSONField(default=list, blank=True)
    reasoning = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "generated_at"]),
        ]
