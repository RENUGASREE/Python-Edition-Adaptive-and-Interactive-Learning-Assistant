from django.db import models
from core.models import User


class Badge(models.Model):
    code = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()


class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)


class XpEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class Streak(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_active = models.DateField(null=True, blank=True)
