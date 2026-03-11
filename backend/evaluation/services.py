import logging
import math
import os
from django.db.models import Avg
from django.utils import timezone
from core.models import User, UserMastery
from assessments.models import DiagnosticQuizAttempt
from recommendation.models import DifficultyShift, UserTopicBehavior
from .models import RecommendationStrategyAssignment, RecommendationEvent, RecommendationOutcome

logger = logging.getLogger("evaluation.metrics")


def get_or_assign_strategy(user: User) -> RecommendationStrategyAssignment:
    assignment = RecommendationStrategyAssignment.objects.filter(user=user).first()
    if assignment:
        return assignment
    bucket = "A" if (user.id % 2) == 0 else "B"
    assignment = RecommendationStrategyAssignment.objects.create(
        user=user,
        strategy_name=bucket,
        strategy_version="v1",
    )
    return assignment


def log_recommendation_event(user: User, algorithm_name: str, recommended_lesson_id: int | None, recommended_topic: str | None, confidence: float):
    assignment = get_or_assign_strategy(user)
    event = RecommendationEvent.objects.create(
        user=user,
        strategy_name=assignment.strategy_name,
        strategy_version=assignment.strategy_version,
        algorithm_name=algorithm_name,
        recommended_lesson_id=recommended_lesson_id,
        recommended_topic=recommended_topic,
        recommendation_confidence=confidence,
    )
    RecommendationOutcome.objects.create(
        event=event,
        user=user,
        completion_rate=0.0,
    )
    return event


def _find_latest_event(user: User, lesson_id: int | None):
    queryset = RecommendationEvent.objects.filter(user=user)
    if lesson_id is not None:
        queryset = queryset.filter(recommended_lesson_id=lesson_id)
    return queryset.order_by("-created_at").first()


def mark_recommendation_accepted(user: User, lesson_id: int):
    event = _find_latest_event(user, lesson_id)
    if not event:
        return None
    outcome = RecommendationOutcome.objects.filter(event=event).first()
    if not outcome:
        outcome = RecommendationOutcome.objects.create(event=event, user=user, completion_rate=0.0)
    if not outcome.accepted:
        outcome.accepted = True
        outcome.accepted_at = timezone.now()
        outcome.save(update_fields=["accepted", "accepted_at"])
    return outcome


def mark_recommendation_completed(user: User, lesson_id: int, mastery_before: float | None, mastery_after: float | None):
    event = _find_latest_event(user, lesson_id)
    if not event:
        return None
    outcome = RecommendationOutcome.objects.filter(event=event).first()
    if not outcome:
        outcome = RecommendationOutcome.objects.create(event=event, user=user, completion_rate=0.0)
    if not outcome.accepted:
        outcome.accepted = True
        outcome.accepted_at = timezone.now()
    outcome.completed = True
    outcome.completed_at = timezone.now()
    outcome.completion_rate = 1.0
    outcome.mastery_before = mastery_before
    outcome.mastery_after = mastery_after
    if mastery_before is not None and mastery_after is not None:
        outcome.mastery_delta = round(mastery_after - mastery_before, 4)
    outcome.save(update_fields=["accepted", "accepted_at", "completed", "completed_at", "completion_rate", "mastery_before", "mastery_after", "mastery_delta"])
    return outcome


def _learning_gain_for_user(user: User) -> float:
    attempts = DiagnosticQuizAttempt.objects.filter(user=user).order_by("created_at")
    if attempts.count() < 2:
        return 0.0
    first = attempts.first().overall_score
    last = attempts.last().overall_score
    if first is None or last is None:
        return 0.0
    return round(float(last) - float(first), 4)


def _mastery_slope_for_user(user: User) -> float:
    outcomes = RecommendationOutcome.objects.filter(user=user, mastery_delta__isnull=False).order_by("completed_at")
    if outcomes.count() < 2:
        return 0.0
    first = outcomes.first()
    last = outcomes.last()
    if not first.completed_at or not last.completed_at:
        return 0.0
    delta = (last.mastery_after or 0.0) - (first.mastery_before or 0.0)
    delta_seconds = (last.completed_at - first.completed_at).total_seconds()
    if delta_seconds <= 0:
        return 0.0
    days = delta_seconds / 86400.0
    if days <= 0:
        return 0.0
    return round(delta / days, 4)


def _time_to_mastery_for_user(user: User) -> float | None:
    mastered = UserMastery.objects.filter(user=user, mastery_score__gte=0.8).order_by("last_updated")
    if not mastered.exists():
        return None
    first_time = mastered.first().last_updated
    if not first_time:
        return None
    delta_seconds = (first_time - user.date_joined).total_seconds()
    if delta_seconds <= 0:
        return None
    days = delta_seconds / 86400.0
    return round(days, 4)


def _engagement_growth_for_user(user: User) -> float:
    delta_seconds = (timezone.now() - user.date_joined).total_seconds()
    if delta_seconds <= 0:
        return 0.0
    days = delta_seconds / 86400.0
    if days <= 0:
        return 0.0
    return round((user.engagement_score or 0.0) / days, 4)


def _recommendation_precision(queryset):
    accepted = queryset.filter(accepted=True).count()
    if accepted == 0:
        return 0.0
    completed = queryset.filter(completed=True).count()
    return round(completed / accepted, 4)


def _mean(values):
    filtered = [value for value in values if isinstance(value, (int, float))]
    if not filtered:
        return 0.0
    return math.fsum(filtered) / len(filtered)


def _sample_variance(values):
    filtered = [value for value in values if isinstance(value, (int, float))]
    n = len(filtered)
    if n < 2:
        return 0.0
    avg = _mean(filtered)
    return math.fsum((val - avg) ** 2 for val in filtered) / (n - 1)


def _log_beta(a: float, b: float) -> float:
    return math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)


def _betacf(a: float, b: float, x: float) -> float:
    max_iter = 200
    eps = 3e-7
    fpmin = 1e-30
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - (qab * x / qap)
    if abs(d) < fpmin:
        d = fpmin
    d = 1.0 / d
    h = d
    for m in range(1, max_iter + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return h


def _regularized_beta(a: float, b: float, x: float) -> float:
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    ln_beta = _log_beta(a, b)
    front = math.exp(a * math.log(x) + b * math.log(1 - x) - ln_beta) / a
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x)
    return 1.0 - front * _betacf(b, a, 1.0 - x)


def _student_t_cdf(t_value: float, df: float) -> float:
    if df <= 0:
        return 0.5
    if t_value == 0:
        return 0.5
    x = df / (df + t_value * t_value)
    a = df / 2.0
    b = 0.5
    ib = _regularized_beta(a, b, x)
    if t_value > 0:
        return 1.0 - 0.5 * ib
    return 0.5 * ib


def _t_critical(df: float, alpha: float = 0.05) -> float:
    target = 1.0 - alpha / 2.0
    low = 0.0
    high = 1.0
    while _student_t_cdf(high, df) < target and high < 1e6:
        high *= 2.0
    for _ in range(80):
        mid = (low + high) / 2.0
        if _student_t_cdf(mid, df) < target:
            low = mid
        else:
            high = mid
    return high


def _independent_ttest(group_a, group_b):
    n1 = len(group_a)
    n2 = len(group_b)
    if n1 < 2 or n2 < 2:
        return {"t_stat": None, "df": None, "p_value": None}
    mean1 = _mean(group_a)
    mean2 = _mean(group_b)
    var1 = _sample_variance(group_a)
    var2 = _sample_variance(group_b)
    se1 = var1 / n1
    se2 = var2 / n2
    denom = math.sqrt(se1 + se2)
    if denom == 0.0:
        if mean1 == mean2:
            return {"t_stat": 0.0, "df": None, "p_value": 1.0}
        return {"t_stat": None, "df": None, "p_value": None}
    t_stat = (mean1 - mean2) / denom
    df_num = (se1 + se2) ** 2
    df_den = (se1 ** 2) / (n1 - 1) + (se2 ** 2) / (n2 - 1)
    if df_den == 0.0:
        return {"t_stat": t_stat, "df": None, "p_value": None}
    df = df_num / df_den
    cdf = _student_t_cdf(abs(t_stat), df)
    p_value = max(0.0, min(1.0, 2.0 * (1.0 - cdf)))
    return {"t_stat": round(t_stat, 6), "df": round(df, 4), "p_value": round(p_value, 6)}


def _cohen_d(group_a, group_b):
    n1 = len(group_a)
    n2 = len(group_b)
    if n1 < 2 or n2 < 2:
        return None
    mean1 = _mean(group_a)
    mean2 = _mean(group_b)
    var1 = _sample_variance(group_a)
    var2 = _sample_variance(group_b)
    pooled_num = ((n1 - 1) * var1) + ((n2 - 1) * var2)
    pooled_den = n1 + n2 - 2
    if pooled_den <= 0:
        return None
    pooled = pooled_num / pooled_den
    if pooled == 0.0:
        return 0.0 if mean1 == mean2 else None
    return round((mean1 - mean2) / math.sqrt(pooled), 6)


def _mean_confidence_interval(values, alpha: float = 0.05):
    n = len(values)
    if n < 2:
        return None
    avg = _mean(values)
    var = _sample_variance(values)
    se = math.sqrt(var / n)
    if se == 0.0:
        return {"mean": round(avg, 6), "lower": round(avg, 6), "upper": round(avg, 6), "n": n}
    t_crit = _t_critical(n - 1, alpha=alpha)
    margin = t_crit * se
    return {"mean": round(avg, 6), "lower": round(avg - margin, 6), "upper": round(avg + margin, 6), "n": n}


def _stat_value(value, sufficient: bool) -> dict:
    return {"value": value if sufficient else None, "insufficient_data": not sufficient}


def _effect_value(value, sufficient: bool) -> dict:
    return {"cohen_d": value if sufficient else None, "insufficient_data": not sufficient}


def _confidence_interval_value(values) -> dict:
    interval = _mean_confidence_interval(values)
    sufficient = interval is not None
    return {"interval": interval, "insufficient_data": not sufficient}

def _group_summary(group_values: dict) -> dict:
    summary = {}
    for group, metrics in group_values.items():
        summary[group] = {
            "learning_gain": {"mean": round(_mean(metrics.get("learning_gain", [])), 6), "n": len(metrics.get("learning_gain", []))},
            "mastery_slope": {"mean": round(_mean(metrics.get("mastery_slope", [])), 6), "n": len(metrics.get("mastery_slope", []))},
            "engagement_growth": {"mean": round(_mean(metrics.get("engagement_growth", [])), 6), "n": len(metrics.get("engagement_growth", []))},
        }
    return summary


def _better_group(group_summary: dict, metric: str) -> str | None:
    a_val = group_summary.get("A", {}).get(metric, {}).get("mean")
    b_val = group_summary.get("B", {}).get(metric, {}).get("mean")
    if a_val is None or b_val is None:
        return None
    if a_val == b_val:
        return "tie"
    return "A" if a_val > b_val else "B"


def _effect_size_label(value: float | None) -> str | None:
    if value is None:
        return None
    magnitude = abs(value)
    if magnitude < 0.2:
        return "negligible"
    if magnitude < 0.5:
        return "small"
    if magnitude < 0.8:
        return "medium"
    return "large"


def _interpret_p_value(p_value: float | None) -> str:
    if p_value is None:
        return "insufficient data"
    if p_value < 0.001:
        return "statistically significant (p < 0.001)"
    if p_value < 0.01:
        return "statistically significant (p < 0.01)"
    if p_value < 0.05:
        return "statistically significant (p < 0.05)"
    return "not statistically significant (p ≥ 0.05)"


def _evaluation_time_range():
    candidates = []
    first_event = RecommendationEvent.objects.order_by("created_at").first()
    last_event = RecommendationEvent.objects.order_by("-created_at").first()
    if first_event and first_event.created_at:
        candidates.append(first_event.created_at)
    if last_event and last_event.created_at:
        candidates.append(last_event.created_at)
    first_shift = DifficultyShift.objects.order_by("created_at").first()
    last_shift = DifficultyShift.objects.order_by("-created_at").first()
    if first_shift and first_shift.created_at:
        candidates.append(first_shift.created_at)
    if last_shift and last_shift.created_at:
        candidates.append(last_shift.created_at)
    first_attempt = DiagnosticQuizAttempt.objects.order_by("created_at").first()
    last_attempt = DiagnosticQuizAttempt.objects.order_by("-created_at").first()
    if first_attempt and first_attempt.created_at:
        candidates.append(first_attempt.created_at)
    if last_attempt and last_attempt.created_at:
        candidates.append(last_attempt.created_at)
    first_outcome = RecommendationOutcome.objects.filter(completed_at__isnull=False).order_by("completed_at").first()
    last_outcome = RecommendationOutcome.objects.filter(completed_at__isnull=False).order_by("-completed_at").first()
    if first_outcome and first_outcome.completed_at:
        candidates.append(first_outcome.completed_at)
    if last_outcome and last_outcome.completed_at:
        candidates.append(last_outcome.completed_at)
    if not candidates:
        return {"start": None, "end": None}
    start = min(candidates)
    end = max(candidates)
    return {"start": start.isoformat(), "end": end.isoformat()}


def _build_research_summary(metrics: dict) -> dict:
    p_values = metrics.get("p_values", {})
    effect_sizes = metrics.get("effect_sizes", {})
    group_summary = metrics.get("ab_group_comparison", {})
    learning_p = p_values.get("learning_gain", {}).get("value")
    slope_p = p_values.get("mastery_slope", {}).get("value")
    engagement_p = p_values.get("engagement_growth", {}).get("value")
    learning_d = effect_sizes.get("learning_gain", {}).get("cohen_d")
    slope_d = effect_sizes.get("mastery_slope", {}).get("cohen_d")
    better = {
        "learning_gain": _better_group(group_summary, "learning_gain"),
        "mastery_slope": _better_group(group_summary, "mastery_slope"),
        "engagement_growth": _better_group(group_summary, "engagement_growth"),
    }
    overall = better.get("learning_gain") if better.get("learning_gain") not in [None, "tie"] else better.get("mastery_slope")
    better["overall"] = overall if overall in ["A", "B"] else "tie"
    practical = {
        "learning_gain": _effect_size_label(learning_d),
        "mastery_slope": _effect_size_label(slope_d),
    }
    summary_text = "Learning gain comparison is " + _interpret_p_value(learning_p) + ". "
    summary_text += "Mastery slope comparison is " + _interpret_p_value(slope_p) + ". "
    summary_text += "Engagement growth comparison is " + _interpret_p_value(engagement_p) + "."
    return {
        "summary_text": summary_text,
        "better_group": better,
        "practical_significance": practical,
    }


def _difficulty_rank(difficulty: str) -> int:
    level = (difficulty or "").strip().lower()
    mapping = {
        "beginner": 1,
        "intermediate": 2,
        "advanced": 3,
        "pro": 3,
        "challenge": 4,
    }
    return mapping.get(level, 1)


def _difficulty_shift_metrics():
    shifts = list(DifficultyShift.objects.all())
    if not shifts:
        return {
            "total_downgrades": 0,
            "total_upgrades": 0,
            "average_difficulty_per_user": 0.0,
            "difficulty_shift_success_rate": 0.0,
            "downgrade_effectiveness": {"success_rate": 0.0, "total": 0, "evaluated": 0},
            "challenge_problem_success_rate": 0.0,
        }

    total_downgrades = 0
    total_upgrades = 0
    downgrade_success = 0
    downgrade_evaluated = 0
    challenge_success = 0
    challenge_evaluated = 0
    per_user = {}

    for shift in shifts:
        from_rank = _difficulty_rank(shift.from_difficulty)
        to_rank = _difficulty_rank(shift.to_difficulty)
        per_user.setdefault(shift.user_id, []).append(to_rank)
        if to_rank < from_rank:
            total_downgrades += 1
            if shift.success is not None:
                downgrade_evaluated += 1
                if shift.success:
                    downgrade_success += 1
        elif to_rank > from_rank:
            total_upgrades += 1
        if (shift.to_difficulty or "").strip().lower() == "challenge":
            if shift.success is not None:
                challenge_evaluated += 1
                if shift.success:
                    challenge_success += 1

    avg_per_user = [sum(values) / len(values) for values in per_user.values() if values]
    average_difficulty_per_user = round(sum(avg_per_user) / len(avg_per_user), 4) if avg_per_user else 0.0
    difficulty_shift_success_rate = round((downgrade_success / downgrade_evaluated), 4) if downgrade_evaluated else 0.0
    challenge_problem_success_rate = round((challenge_success / challenge_evaluated), 4) if challenge_evaluated else 0.0

    return {
        "total_downgrades": total_downgrades,
        "total_upgrades": total_upgrades,
        "average_difficulty_per_user": average_difficulty_per_user,
        "difficulty_shift_success_rate": difficulty_shift_success_rate,
        "downgrade_effectiveness": {
            "success_rate": difficulty_shift_success_rate,
            "total": total_downgrades,
            "evaluated": downgrade_evaluated,
        },
        "challenge_problem_success_rate": challenge_problem_success_rate,
    }


def _velocity_distribution():
    behaviors = list(UserTopicBehavior.objects.all())
    if not behaviors:
        return {"low": 0, "medium": 0, "high": 0, "mean": 0.0, "total": 0}
    low = float(os.getenv("VELOCITY_LOW_THRESHOLD", "0.00005"))
    high = float(os.getenv("VELOCITY_HIGH_THRESHOLD", "0.0002"))
    low_count = 0
    high_count = 0
    total = 0
    total_value = 0.0
    for behavior in behaviors:
        total += 1
        velocity = float(behavior.velocity_avg or 0.0)
        total_value += velocity
        if velocity <= low:
            low_count += 1
        elif velocity >= high:
            high_count += 1
    medium_count = max(total - low_count - high_count, 0)
    return {
        "low": low_count,
        "medium": medium_count,
        "high": high_count,
        "mean": round(total_value / total, 6) if total else 0.0,
        "total": total,
    }


def system_evaluation_metrics():
    try:
        users = list(User.objects.all())
    except Exception:
        logger.exception("evaluation_users_fetch_failed")
        users = []
    if not users:
        return {
            "mean_learning_gain": 0.0,
            "recommendation_precision": 0.0,
            "engagement_improvement": 0.0,
            "average_time_to_mastery": 0.0,
            "mastery_improvement_slope": 0.0,
            "ab_results": {},
            "total_downgrades": 0,
            "total_upgrades": 0,
            "average_difficulty_per_user": 0.0,
            "difficulty_shift_success_rate": 0.0,
            "velocity_distribution": {"low": 0, "medium": 0, "high": 0, "mean": 0.0, "total": 0},
            "downgrade_effectiveness": {"success_rate": 0.0, "total": 0, "evaluated": 0},
            "challenge_problem_success_rate": 0.0,
            "p_values": {
                "learning_gain": _stat_value(None, False),
                "mastery_slope": _stat_value(None, False),
                "engagement_growth": _stat_value(None, False),
            },
            "effect_sizes": {
                "learning_gain": _effect_value(None, False),
                "mastery_slope": _effect_value(None, False),
            },
            "confidence_intervals": {
                "mean_learning_gain": _confidence_interval_value([]),
                "mean_time_to_mastery": _confidence_interval_value([]),
            },
            "ab_group_comparison": {},
            "data_snapshot": {
                "total_users": 0,
                "total_recommendations": 0,
                "total_difficulty_shifts": 0,
                "evaluation_time_range": {"start": None, "end": None},
            },
        }

    try:
        learning_gains = []
        engagement_growth = []
        slopes = []
        times = []
        user_metrics = {}
        for user in users:
            try:
                learning_gain = _learning_gain_for_user(user)
                engagement = _engagement_growth_for_user(user)
                slope = _mastery_slope_for_user(user)
                time_to_mastery = _time_to_mastery_for_user(user)
                learning_gains.append(learning_gain)
                engagement_growth.append(engagement)
                slopes.append(slope)
                if time_to_mastery is not None:
                    times.append(time_to_mastery)
                user_metrics[user.id] = {
                    "learning_gain": learning_gain,
                    "engagement_growth": engagement,
                    "mastery_slope": slope,
                    "time_to_mastery": time_to_mastery,
                }
            except Exception:
                logger.exception("evaluation_user_metrics_failed", extra={"user_id": user.id})

        try:
            outcomes = RecommendationOutcome.objects.all()
        except Exception:
            logger.exception("evaluation_outcomes_fetch_failed")
            outcomes = RecommendationOutcome.objects.none()
        precision = _recommendation_precision(outcomes)

        assignments = RecommendationStrategyAssignment.objects.values_list("strategy_name", flat=True).distinct()
        ab_results = {}
        for strategy in assignments:
            try:
                strategy_users = RecommendationStrategyAssignment.objects.filter(strategy_name=strategy).values_list("user_id", flat=True)
                subset = outcomes.filter(user_id__in=strategy_users)
                ab_results[strategy] = {
                    "recommendation_precision": _recommendation_precision(subset),
                    "completion_rate": round(subset.aggregate(avg=Avg("completion_rate"))["avg"] or 0.0, 4),
                    "average_mastery_delta": round(subset.aggregate(avg=Avg("mastery_delta"))["avg"] or 0.0, 4),
                }
            except Exception:
                logger.exception("evaluation_ab_results_failed", extra={"strategy": strategy})

        group_values = {}
        for assignment in RecommendationStrategyAssignment.objects.all():
            metrics = user_metrics.get(assignment.user_id)
            if not metrics:
                continue
            group = assignment.strategy_name
            if group not in group_values:
                group_values[group] = {
                    "learning_gain": [],
                    "mastery_slope": [],
                    "engagement_growth": [],
                }
            group_values[group]["learning_gain"].append(metrics["learning_gain"])
            group_values[group]["mastery_slope"].append(metrics["mastery_slope"])
            group_values[group]["engagement_growth"].append(metrics["engagement_growth"])

        group_a = group_values.get("A", {})
        group_b = group_values.get("B", {})
        learning_test = _independent_ttest(group_a.get("learning_gain", []), group_b.get("learning_gain", []))
        slope_test = _independent_ttest(group_a.get("mastery_slope", []), group_b.get("mastery_slope", []))
        engagement_test = _independent_ttest(group_a.get("engagement_growth", []), group_b.get("engagement_growth", []))
        confidence_intervals = {
            "mean_learning_gain": _confidence_interval_value(learning_gains),
            "mean_time_to_mastery": _confidence_interval_value(times),
        }
        ab_group_comparison = _group_summary(group_values)

        try:
            difficulty_metrics = _difficulty_shift_metrics()
        except Exception:
            logger.exception("evaluation_difficulty_metrics_failed")
            difficulty_metrics = {
                "total_downgrades": 0,
                "total_upgrades": 0,
                "average_difficulty_per_user": 0.0,
                "difficulty_shift_success_rate": 0.0,
                "downgrade_effectiveness": {"success_rate": 0.0, "total": 0, "evaluated": 0},
                "challenge_problem_success_rate": 0.0,
            }
        learning_sufficient = len(group_a.get("learning_gain", [])) >= 2 and len(group_b.get("learning_gain", [])) >= 2
        slope_sufficient = len(group_a.get("mastery_slope", [])) >= 2 and len(group_b.get("mastery_slope", [])) >= 2
        engagement_sufficient = len(group_a.get("engagement_growth", [])) >= 2 and len(group_b.get("engagement_growth", [])) >= 2
        return {
            "mean_learning_gain": round(_mean(learning_gains), 4),
            "recommendation_precision": precision,
            "engagement_improvement": round(_mean(engagement_growth), 4),
            "average_time_to_mastery": round(_mean(times), 4) if times else 0.0,
            "mastery_improvement_slope": round(_mean(slopes), 4),
            "ab_results": ab_results,
            "total_downgrades": difficulty_metrics["total_downgrades"],
            "total_upgrades": difficulty_metrics["total_upgrades"],
            "average_difficulty_per_user": difficulty_metrics["average_difficulty_per_user"],
            "difficulty_shift_success_rate": difficulty_metrics["difficulty_shift_success_rate"],
            "velocity_distribution": _velocity_distribution(),
            "downgrade_effectiveness": difficulty_metrics["downgrade_effectiveness"],
            "challenge_problem_success_rate": difficulty_metrics["challenge_problem_success_rate"],
            "p_values": {
                "learning_gain": _stat_value(learning_test["p_value"], learning_sufficient),
                "mastery_slope": _stat_value(slope_test["p_value"], slope_sufficient),
                "engagement_growth": _stat_value(engagement_test["p_value"], engagement_sufficient),
            },
            "effect_sizes": {
                "learning_gain": _effect_value(_cohen_d(group_a.get("learning_gain", []), group_b.get("learning_gain", [])), learning_sufficient),
                "mastery_slope": _effect_value(_cohen_d(group_a.get("mastery_slope", []), group_b.get("mastery_slope", [])), slope_sufficient),
            },
            "confidence_intervals": confidence_intervals,
            "ab_group_comparison": ab_group_comparison,
            "data_snapshot": {
                "total_users": len(users),
                "total_recommendations": RecommendationEvent.objects.count(),
                "total_difficulty_shifts": DifficultyShift.objects.count(),
                "evaluation_time_range": _evaluation_time_range(),
            },
        }
    except Exception:
        logger.exception("system_evaluation_metrics_failed")
        return {
            "mean_learning_gain": 0.0,
            "recommendation_precision": 0.0,
            "engagement_improvement": 0.0,
            "average_time_to_mastery": 0.0,
            "mastery_improvement_slope": 0.0,
            "ab_results": {},
            "total_downgrades": 0,
            "total_upgrades": 0,
            "average_difficulty_per_user": 0.0,
            "difficulty_shift_success_rate": 0.0,
            "velocity_distribution": {"low": 0, "medium": 0, "high": 0, "mean": 0.0, "total": 0},
            "downgrade_effectiveness": {"success_rate": 0.0, "total": 0, "evaluated": 0},
            "challenge_problem_success_rate": 0.0,
            "p_values": {
                "learning_gain": _stat_value(None, False),
                "mastery_slope": _stat_value(None, False),
                "engagement_growth": _stat_value(None, False),
            },
            "effect_sizes": {
                "learning_gain": _effect_value(None, False),
                "mastery_slope": _effect_value(None, False),
            },
            "confidence_intervals": {
                "mean_learning_gain": _confidence_interval_value([]),
                "mean_time_to_mastery": _confidence_interval_value([]),
            },
            "ab_group_comparison": {},
            "data_snapshot": {
                "total_users": 0,
                "total_recommendations": 0,
                "total_difficulty_shifts": 0,
                "evaluation_time_range": {"start": None, "end": None},
            },
        }


def export_system_metrics():
    metrics = system_evaluation_metrics()
    rows = [
        ["metric", "value"],
        ["mean_learning_gain", metrics["mean_learning_gain"]],
        ["recommendation_precision", metrics["recommendation_precision"]],
        ["engagement_improvement", metrics["engagement_improvement"]],
        ["average_time_to_mastery", metrics["average_time_to_mastery"]],
        ["mastery_improvement_slope", metrics["mastery_improvement_slope"]],
    ]
    rows.append(["p_value_learning_gain", metrics["p_values"]["learning_gain"]["value"]])
    rows.append(["p_value_learning_gain_insufficient_data", metrics["p_values"]["learning_gain"]["insufficient_data"]])
    rows.append(["p_value_mastery_slope", metrics["p_values"]["mastery_slope"]["value"]])
    rows.append(["p_value_mastery_slope_insufficient_data", metrics["p_values"]["mastery_slope"]["insufficient_data"]])
    rows.append(["p_value_engagement_growth", metrics["p_values"]["engagement_growth"]["value"]])
    rows.append(["p_value_engagement_growth_insufficient_data", metrics["p_values"]["engagement_growth"]["insufficient_data"]])
    rows.append(["effect_size_learning_gain_cohen_d", metrics["effect_sizes"]["learning_gain"]["cohen_d"]])
    rows.append(["effect_size_learning_gain_insufficient_data", metrics["effect_sizes"]["learning_gain"]["insufficient_data"]])
    rows.append(["effect_size_mastery_slope_cohen_d", metrics["effect_sizes"]["mastery_slope"]["cohen_d"]])
    rows.append(["effect_size_mastery_slope_insufficient_data", metrics["effect_sizes"]["mastery_slope"]["insufficient_data"]])
    ci_gain = metrics["confidence_intervals"]["mean_learning_gain"]["interval"]
    rows.append(["ci_mean_learning_gain_mean", ci_gain["mean"] if ci_gain else None])
    rows.append(["ci_mean_learning_gain_lower", ci_gain["lower"] if ci_gain else None])
    rows.append(["ci_mean_learning_gain_upper", ci_gain["upper"] if ci_gain else None])
    rows.append(["ci_mean_learning_gain_n", ci_gain["n"] if ci_gain else 0])
    rows.append(["ci_mean_learning_gain_insufficient_data", metrics["confidence_intervals"]["mean_learning_gain"]["insufficient_data"]])
    ci_time = metrics["confidence_intervals"]["mean_time_to_mastery"]["interval"]
    rows.append(["ci_mean_time_to_mastery_mean", ci_time["mean"] if ci_time else None])
    rows.append(["ci_mean_time_to_mastery_lower", ci_time["lower"] if ci_time else None])
    rows.append(["ci_mean_time_to_mastery_upper", ci_time["upper"] if ci_time else None])
    rows.append(["ci_mean_time_to_mastery_n", ci_time["n"] if ci_time else 0])
    rows.append(["ci_mean_time_to_mastery_insufficient_data", metrics["confidence_intervals"]["mean_time_to_mastery"]["insufficient_data"]])
    rows.append(["ab_group_A_learning_gain_mean", metrics["ab_group_comparison"].get("A", {}).get("learning_gain", {}).get("mean")])
    rows.append(["ab_group_A_learning_gain_n", metrics["ab_group_comparison"].get("A", {}).get("learning_gain", {}).get("n")])
    rows.append(["ab_group_B_learning_gain_mean", metrics["ab_group_comparison"].get("B", {}).get("learning_gain", {}).get("mean")])
    rows.append(["ab_group_B_learning_gain_n", metrics["ab_group_comparison"].get("B", {}).get("learning_gain", {}).get("n")])
    rows.append(["ab_group_A_mastery_slope_mean", metrics["ab_group_comparison"].get("A", {}).get("mastery_slope", {}).get("mean")])
    rows.append(["ab_group_A_mastery_slope_n", metrics["ab_group_comparison"].get("A", {}).get("mastery_slope", {}).get("n")])
    rows.append(["ab_group_B_mastery_slope_mean", metrics["ab_group_comparison"].get("B", {}).get("mastery_slope", {}).get("mean")])
    rows.append(["ab_group_B_mastery_slope_n", metrics["ab_group_comparison"].get("B", {}).get("mastery_slope", {}).get("n")])
    rows.append(["ab_group_A_engagement_growth_mean", metrics["ab_group_comparison"].get("A", {}).get("engagement_growth", {}).get("mean")])
    rows.append(["ab_group_A_engagement_growth_n", metrics["ab_group_comparison"].get("A", {}).get("engagement_growth", {}).get("n")])
    rows.append(["ab_group_B_engagement_growth_mean", metrics["ab_group_comparison"].get("B", {}).get("engagement_growth", {}).get("mean")])
    rows.append(["ab_group_B_engagement_growth_n", metrics["ab_group_comparison"].get("B", {}).get("engagement_growth", {}).get("n")])
    rows.append(["snapshot_total_users", metrics["data_snapshot"]["total_users"]])
    rows.append(["snapshot_total_recommendations", metrics["data_snapshot"]["total_recommendations"]])
    rows.append(["snapshot_total_difficulty_shifts", metrics["data_snapshot"]["total_difficulty_shifts"]])
    rows.append(["snapshot_evaluation_start", metrics["data_snapshot"]["evaluation_time_range"]["start"]])
    rows.append(["snapshot_evaluation_end", metrics["data_snapshot"]["evaluation_time_range"]["end"]])
    for strategy, result in metrics["ab_results"].items():
        rows.append([f"{strategy}_recommendation_precision", result["recommendation_precision"]])
        rows.append([f"{strategy}_completion_rate", result["completion_rate"]])
        rows.append([f"{strategy}_average_mastery_delta", result["average_mastery_delta"]])
    return rows


def system_evaluation_summary():
    try:
        metrics = system_evaluation_metrics()
        summary = _build_research_summary(metrics)
        return {
            "summary_text": summary["summary_text"],
            "better_group": summary["better_group"],
            "practical_significance": summary["practical_significance"],
            "p_values": metrics["p_values"],
            "effect_sizes": metrics["effect_sizes"],
            "confidence_intervals": metrics["confidence_intervals"],
            "ab_group_comparison": metrics["ab_group_comparison"],
            "data_snapshot": metrics["data_snapshot"],
        }
    except Exception:
        logger.exception("system_evaluation_summary_failed")
        return {
            "summary_text": "Evaluation summary unavailable due to insufficient data.",
            "better_group": {"learning_gain": None, "mastery_slope": None, "engagement_growth": None, "overall": None},
            "practical_significance": {"learning_gain": None, "mastery_slope": None},
            "p_values": {
                "learning_gain": _stat_value(None, False),
                "mastery_slope": _stat_value(None, False),
                "engagement_growth": _stat_value(None, False),
            },
            "effect_sizes": {
                "learning_gain": _effect_value(None, False),
                "mastery_slope": _effect_value(None, False),
            },
            "confidence_intervals": {
                "mean_learning_gain": _confidence_interval_value([]),
                "mean_time_to_mastery": _confidence_interval_value([]),
            },
            "ab_group_comparison": {},
            "data_snapshot": {
                "total_users": 0,
                "total_recommendations": 0,
                "total_difficulty_shifts": 0,
                "evaluation_time_range": {"start": None, "end": None},
            },
        }
