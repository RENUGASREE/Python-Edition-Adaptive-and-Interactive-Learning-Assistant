"""Analytics computations for mastery, engagement, and risk signals."""
import logging
from assessments.models import DiagnosticQuizAttempt, AssessmentInteraction
from core.models import User

logger = logging.getLogger("analytics.metrics")


def mastery_progression(user: User):
    try:
        return sorted(
            DiagnosticQuizAttempt.objects.filter(user=user).values("created_at", "overall_score"),
            key=lambda item: item["created_at"],
        )
    except Exception:
        logger.exception("analytics_mastery_progression_failed", extra={"user_id": user.id})
        return []


def interaction_mastery_series(user: User):
    try:
        interactions = AssessmentInteraction.objects.filter(user=user).order_by("created_at")[:200]
        series = []
        for interaction in interactions:
            series.append({
                "created_at": interaction.created_at,
                "topic": interaction.topic,
                "correctness": interaction.correctness,
            })
        return series
    except Exception:
        logger.exception("analytics_interaction_series_failed", extra={"user_id": user.id})
        return []


def learning_gain(user: User):
    try:
        attempts = DiagnosticQuizAttempt.objects.filter(user=user).order_by("created_at")
        if attempts.count() < 2:
            return 0.0
        first = attempts.first().overall_score
        last = attempts.last().overall_score
        if first is None or last is None:
            return 0.0
        return round(float(last) - float(first), 4)
    except Exception:
        logger.exception("analytics_learning_gain_failed", extra={"user_id": user.id})
        return 0.0


def strongest_weakest_topics(user: User):
    try:
        mastery = user.mastery_vector or {}
        if not mastery:
            return None, None
        filtered = [(key, value) for key, value in mastery.items() if value is not None]
        if not filtered:
            return None, None
        sorted_items = sorted(filtered, key=lambda item: item[1])
        weakest = sorted_items[0][0]
        strongest = sorted_items[-1][0]
        return weakest, strongest
    except Exception:
        logger.exception("analytics_strongest_weakest_failed", extra={"user_id": user.id})
        return None, None


def engagement_index(user: User):
    try:
        engagement = user.engagement_score or 0.0
        interactions = AssessmentInteraction.objects.filter(user=user).count()
        return round(min(1.0, engagement + (interactions / 100.0)), 4)
    except Exception:
        logger.exception("analytics_engagement_index_failed", extra={"user_id": user.id})
        return 0.0


def risk_score(user: User):
    try:
        mastery = user.mastery_vector or {}
        values = [value for value in mastery.values() if isinstance(value, (int, float))]
        average_mastery = sum(values) / len(values) if values else 0.0
        engagement = user.engagement_score or 0.0
        return round((1 - average_mastery) * 0.6 + (1 - engagement) * 0.4, 4)
    except Exception:
        logger.exception("analytics_risk_score_failed", extra={"user_id": user.id})
        return 0.0
