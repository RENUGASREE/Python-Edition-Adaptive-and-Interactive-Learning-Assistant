from django.db import models
from core.models import User


class RecommendationStrategyAssignment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    strategy_name = models.CharField(max_length=50)
    strategy_version = models.CharField(max_length=20, default="v1")
    assigned_at = models.DateTimeField(auto_now_add=True)


class RecommendationEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    strategy_name = models.CharField(max_length=50)
    strategy_version = models.CharField(max_length=20)
    algorithm_name = models.CharField(max_length=100)
    recommended_lesson_id = models.IntegerField(null=True, blank=True)
    recommended_topic = models.CharField(max_length=255, null=True, blank=True)
    recommendation_confidence = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)


class RecommendationOutcome(models.Model):
    event = models.OneToOneField(RecommendationEvent, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    completion_rate = models.FloatField(default=0.0)
    mastery_before = models.FloatField(null=True, blank=True)
    mastery_after = models.FloatField(null=True, blank=True)
    mastery_delta = models.FloatField(null=True, blank=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
