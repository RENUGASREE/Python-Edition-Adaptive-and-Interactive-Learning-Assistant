"""Service utilities to keep user-centric metrics logic out of views."""
from django.utils import timezone
from core.models import User


def update_engagement(user: User, delta: float) -> float:
    user.engagement_score = max(0.0, min(1.0, (user.engagement_score or 0.0) + delta))
    user.save(update_fields=["engagement_score"])
    return user.engagement_score


def update_learning_velocity(user: User, lesson_duration_minutes: float) -> float:
    current = user.learning_velocity or 0.0
    updated = round((current * 0.7) + (lesson_duration_minutes * 0.3), 4)
    user.learning_velocity = updated
    user.save(update_fields=["learning_velocity"])
    return updated


def mark_diagnostic_completed(user: User) -> None:
    user.diagnostic_completed = True
    user.has_taken_quiz = True
    user.save(update_fields=["diagnostic_completed", "has_taken_quiz"])


def touch_last_active(user: User) -> None:
    user.last_login = timezone.now()
    user.save(update_fields=["last_login"])
