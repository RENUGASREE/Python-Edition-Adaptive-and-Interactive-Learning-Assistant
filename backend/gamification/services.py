"""Gamification helpers to reward engagement and progression."""
from datetime import date
from django.db import models
from .models import Badge, UserBadge, XpEvent, Streak
from core.models import User
from users.services import update_engagement


def award_badge(user: User, code: str):
    badge = Badge.objects.filter(code=code).first()
    if not badge:
        return None
    UserBadge.objects.get_or_create(user=user, badge=badge)
    return badge


def ensure_badges():
    badges = [
        ("loop-master", "Loop Master", "Maintain a 5-day learning streak."),
        ("function-pro", "Function Pro", "Earn 200 XP from practice."),
        ("consistent-learner", "Consistent Learner", "Complete 10 lessons."),
        ("python-pioneer", "Python Pioneer", "Complete all lessons in Module 1."),
        ("data-detective", "Data Detective", "Complete all lessons in Module 2."),
        ("logic-lord", "Logic Lord", "Complete all lessons in Module 3."),
        ("iterative-icon", "Iterative Icon", "Complete all lessons in Module 4."),
        ("code-architect", "Code Architect", "Complete all lessons in Module 5."),
        ("oop-overlord", "OOP Overlord", "Complete all lessons in Module 6."),
        ("topic-wizard", "Topic Wizard", "Reach 95% mastery in any specific topic."),
    ]
    for code, title, description in badges:
        Badge.objects.get_or_create(code=code, defaults={"title": title, "description": description})


def add_xp(user: User, points: int, reason: str):
    XpEvent.objects.create(user=user, points=points, reason=reason)
    update_engagement(user, min(0.02, max(0.005, points / 500)))
    ensure_badges()
    xp_total = XpEvent.objects.filter(user=user).aggregate(total_points=models.Sum("points")).get("total_points") or 0
    if xp_total >= 200:
        award_badge(user, "function-pro")


def update_streak(user: User):
    streak, _ = Streak.objects.get_or_create(user=user)
    today = date.today()
    if streak.last_active == today:
        return streak
    if streak.last_active and (today - streak.last_active).days == 1:
        streak.current_streak += 1
    else:
        streak.current_streak = 1
    streak.longest_streak = max(streak.longest_streak, streak.current_streak)
    streak.last_active = today
    streak.save()
    ensure_badges()
    if streak.current_streak >= 5:
        award_badge(user, "loop-master")
    return streak
