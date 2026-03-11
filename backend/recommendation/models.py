from django.db import models
from core.models import User


class UserTopicBehavior(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    velocity_avg = models.FloatField(default=0.0)
    last_mastery = models.FloatField(null=True, blank=True)
    last_mastery_at = models.DateTimeField(null=True, blank=True)
    failure_streak = models.IntegerField(default=0)
    avg_response_time = models.FloatField(default=0.0)
    avg_hints_used = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True)


class DifficultyShift(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    from_difficulty = models.CharField(max_length=50)
    to_difficulty = models.CharField(max_length=50)
    reason = models.CharField(max_length=100)
    mastery = models.FloatField(null=True, blank=True)
    velocity = models.FloatField(null=True, blank=True)
    failure_streak = models.IntegerField(default=0)
    avg_response_time = models.FloatField(null=True, blank=True)
    avg_hints_used = models.FloatField(null=True, blank=True)
    success = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
