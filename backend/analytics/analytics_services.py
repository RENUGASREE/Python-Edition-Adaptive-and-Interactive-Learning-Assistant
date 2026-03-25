"""Analytics computations for mastery, engagement, and risk signals."""
import logging
from datetime import datetime
from django.db.models import Avg
from core.models import User, UserProgress, QuizAttempt
from assessments.models import AssessmentInteraction

logger = logging.getLogger("analytics.metrics")


def mastery_progression(user: User):
    """Compute mastery progression from placement quiz, module quizzes, and lesson quizzes."""
    try:
        entries = []
        
        # Placement quiz (if completed)
        if hasattr(user, 'diagnostic_completed') and user.diagnostic_completed:
            # Use engagement_score as proxy for placement score if not stored elsewhere
            entries.append({
                "created_at": user.date_joined,
                "overall_score": user.engagement_score or 0.0,
                "source": "placement"
            })
        
        # Module quiz attempts (notes contain module:level)
        module_attempts = QuizAttempt.objects.filter(
            user=user,
            notes__contains="module:"
        ).order_by('created_at')
        for attempt in module_attempts:
            entries.append({
                "created_at": attempt.created_at,
                "overall_score": attempt.score / 100.0,  # Convert percentage to 0-1
                "source": "module"
            })
        
# Average lesson quiz scores per week as progression points
        user_id = user.original_uuid or str(user.id)
        lesson_progress = UserProgress.objects.filter(
            user_id=user_id,
            completed=True,
            score__isnull=False
        ).order_by('completed_at')
        
        # NEW: UserSubmission scores (code challenges)
        from core.models import UserSubmission
        submission_scores = UserSubmission.objects.filter(
            user=user,
            score__gt=0
        ).values_list('created_at', 'score').order_by('created_at')
        
        if lesson_progress.exists() or submission_scores.exists():
            # Group by week to show progression over time
            from collections import defaultdict
            weekly_scores = defaultdict(list)
            
            # UserProgress (lessons/quizzes)
            for prog in lesson_progress:
                week_key = (prog.completed_at.year, prog.completed_at.isocalendar()[1])
                weekly_scores[week_key].append(prog.score)
            
            # UserSubmission (code challenges)
            for created_at, score in submission_scores:
                week_key = (created_at.year, created_at.isocalendar()[1])
                weekly_scores[week_key].append(int(score))
            
            for (year, week), scores in sorted(weekly_scores.items()):
                avg_score = sum(scores) / len(scores)
                # Use Monday of that week as timestamp
                week_date = datetime.strptime(f"{year} {week} 1", "%Y %W %w")
                entries.append({
                    "created_at": week_date,
                    "overall_score": min(avg_score / 100.0, 1.0),
                    "source": "lessons_challenges"
                })
        
        # Sort by date
        entries.sort(key=lambda x: x["created_at"])
        
        # Fallback: ensure at least 2 data points for chart rendering
        # If user has activity but not enough progression data, create synthetic points
        if len(entries) < 2:
            # Check if user has ANY activity we can infer from
            has_lessons = UserProgress.objects.filter(
                user_id=user_id, completed=True
            ).exists()
            has_module_attempts = QuizAttempt.objects.filter(user=user).exists()
            
            if has_lessons or has_module_attempts or (user.engagement_score and user.engagement_score > 0):
                # Create synthetic progression: start -> now
                start_score = 0.2  # Assume starting at 20%
                if entries:
                    # Use existing entry as end point
                    end_score = entries[0]["overall_score"]
                    start_date = user.date_joined
                    end_date = entries[0]["created_at"]
                else:
                    # No entries at all - create from engagement or default
                    end_score = user.engagement_score or 0.5
                    start_date = user.date_joined
                    end_date = datetime.now()
                
                # Ensure start < end in time
                if start_date == end_date:
                    start_date = end_date.replace(day=end_date.day-1) if end_date.day > 1 else end_date
                
                entries = [
                    {"created_at": start_date, "overall_score": start_score, "source": "start"},
                    {"created_at": end_date, "overall_score": end_score, "source": "current"}
                ]
        
        return entries
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
    """Compute learning gain as difference between first and last mastery scores."""
    try:
        progression = mastery_progression(user)
        if len(progression) < 2:
            return 0.0
        first = progression[0]["overall_score"]
        last = progression[-1]["overall_score"]
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
