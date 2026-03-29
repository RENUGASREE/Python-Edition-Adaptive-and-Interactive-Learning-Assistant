"""Recommendation scoring that remains explainable and feature-driven."""
import os
import logging
from django.core.cache import cache
from django.utils import timezone
from assessments.models import AssessmentInteraction
from lessons.models import LessonProfile
from core.models import Lesson, Module, User, UserProgress
from evaluation.services import get_or_assign_strategy, log_recommendation_event
from .models import UserTopicBehavior, DifficultyShift

logger = logging.getLogger("recommendation.engine")


# --- Topic Normalization ---
_CANONICAL_TOPICS = {
    "variables",
    "conditions",
    "loops",
    "functions",
    "data_structures",
    "oop",
}

_TOPIC_SYNONYMS = {
    "variables": ["variable", "data types", "data_types", "basics: variables"],
    "conditions": ["conditionals", "if_statement", "if-else", "if_else", "elif_ladder", "if", "if/else"],
    "loops": ["for_loop", "while_loop", "iteration", "looping"],
    "functions": ["methods", "def_function", "function_basics"],
    "data_structures": ["lists", "tuples", "dicts", "dictionaries", "sets", "data-structures"],
    "oop": ["object_oriented_programming", "object-oriented", "classes", "class_basics", "objects"],
}

_ALIAS_TO_CANONICAL = {}
for canon, aliases in _TOPIC_SYNONYMS.items():
    _ALIAS_TO_CANONICAL[canon] = canon
    for a in aliases:
        _ALIAS_TO_CANONICAL[a] = canon


def normalize_topic(topic: str | None) -> str:
    raw = (topic or "").strip().lower()
    key = raw.replace(" ", "_").replace("-", "_")
    return _ALIAS_TO_CANONICAL.get(key, key if key in _CANONICAL_TOPICS else key)


def compute_priority_score(mastery, recent_failure_rate, prereq_weight, engagement_factor, difficulty_adjustment_factor, velocity_weight, struggle_weight):
    return round(
        (1 - mastery) * 0.35
        + recent_failure_rate * 0.15
        + prereq_weight * 0.15
        + engagement_factor * 0.15
        + (velocity_weight * 0.1)
        + (struggle_weight * 0.1)
        + difficulty_adjustment_factor,
        4,
    )


def compute_priority_score_b(mastery, recent_failure_rate, prereq_weight, engagement_factor, difficulty_adjustment_factor, velocity_weight, struggle_weight):
    return round(
        (1 - mastery) * 0.4
        + recent_failure_rate * 0.1
        + prereq_weight * 0.1
        + engagement_factor * 0.2
        + (velocity_weight * 0.15)
        + (struggle_weight * 0.05)
        + difficulty_adjustment_factor,
        4,
    )


def recent_failure(user: User, topic: str):
    canon = normalize_topic(topic)
    # Include both canonical and known aliases for robustness on existing data
    aliases = [canon]
    for k, v in _TOPIC_SYNONYMS.items():
        if k == canon:
            aliases = [canon] + v
            break
    attempts = AssessmentInteraction.objects.filter(user=user, topic__in=aliases).order_by("-created_at")[:10]
    if not attempts:
        return 0.0
    failures = sum(1 for attempt in attempts if not attempt.correctness)
    return round(failures / len(attempts), 4)


def prerequisite_weight(topic: str):
    profile = LessonProfile.objects.filter(topic=topic).first()
    if not profile or not profile.prerequisites:
        return 0.0
    return min(1.0, 0.2 * len(profile.prerequisites))


def _behavior_alpha() -> float:
    return float(os.getenv("BEHAVIOR_ALPHA", "0.3"))


def _velocity_alpha() -> float:
    return float(os.getenv("VELOCITY_ALPHA", "0.3"))


def get_behavior(user: User, topic: str) -> UserTopicBehavior:
    canon = normalize_topic(topic)
    behavior = UserTopicBehavior.objects.filter(user=user, topic=canon).first()
    if behavior:
        return behavior
    return UserTopicBehavior.objects.create(user=user, topic=canon)


def update_behavior_from_interaction(user: User, topic: str, correctness: bool, time_spent: float, hints_used: int):
    behavior = get_behavior(user, normalize_topic(topic))
    alpha = _behavior_alpha()
    behavior.avg_response_time = round((alpha * float(time_spent)) + ((1 - alpha) * behavior.avg_response_time), 4)
    behavior.avg_hints_used = round((alpha * float(hints_used)) + ((1 - alpha) * behavior.avg_hints_used), 4)
    if correctness:
        behavior.failure_streak = 0
    else:
        behavior.failure_streak = behavior.failure_streak + 1
    behavior.updated_at = timezone.now()
    behavior.save(update_fields=["avg_response_time", "avg_hints_used", "failure_streak", "updated_at"])
    return behavior


def update_topic_velocity(user: User, topic: str, new_mastery: float):
    behavior = get_behavior(user, normalize_topic(topic))
    now = timezone.now()
    if behavior.last_mastery is None or behavior.last_mastery_at is None:
        behavior.last_mastery = float(new_mastery)
        behavior.last_mastery_at = now
        behavior.save(update_fields=["last_mastery", "last_mastery_at"])
        return behavior
    delta = float(new_mastery) - float(behavior.last_mastery)
    seconds = max((now - behavior.last_mastery_at).total_seconds(), 1.0)
    velocity = delta / seconds
    alpha = _velocity_alpha()
    behavior.velocity_avg = round((alpha * velocity) + ((1 - alpha) * behavior.velocity_avg), 6)
    behavior.last_mastery = float(new_mastery)
    behavior.last_mastery_at = now
    behavior.save(update_fields=["velocity_avg", "last_mastery", "last_mastery_at"])
    user_alpha = float(os.getenv("USER_VELOCITY_ALPHA", "0.2"))
    current_overall = user.learning_velocity or 0.0
    user.learning_velocity = round((user_alpha * behavior.velocity_avg) + ((1 - user_alpha) * current_overall), 6)
    user.save(update_fields=["learning_velocity"])
    return behavior


def _velocity_weight(velocity_avg: float) -> float:
    low = float(os.getenv("VELOCITY_LOW_THRESHOLD", "0.00005"))
    high = float(os.getenv("VELOCITY_HIGH_THRESHOLD", "0.0002"))
    if velocity_avg <= low:
        return 0.0
    if velocity_avg >= high:
        return 1.0
    return round((velocity_avg - low) / (high - low), 4)


def _struggle_weight(behavior: UserTopicBehavior) -> float:
    failure_threshold = int(os.getenv("FAILURE_STREAK_THRESHOLD", "3"))
    high_time = float(os.getenv("RESPONSE_TIME_HIGH_SECONDS", "40"))
    high_hints = float(os.getenv("HINTS_HIGH_THRESHOLD", "2"))
    score = 0.0
    if behavior.failure_streak >= failure_threshold:
        score += 0.5
    if behavior.avg_response_time >= high_time:
        score += 0.3
    if behavior.avg_hints_used >= high_hints:
        score += 0.2
    return min(1.0, round(score, 4))


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


def _downgrade_target(base_difficulty: str) -> str:
    rank = _difficulty_rank(base_difficulty)
    if rank <= 1:
        return base_difficulty or "Beginner"
    if rank == 2:
        return "Beginner"
    if rank == 3:
        return "Intermediate"
    return "Advanced"


def compute_difficulty_adjustment(mastery: float, behavior: UserTopicBehavior, base_difficulty: str):
    low_velocity = float(os.getenv("VELOCITY_LOW_THRESHOLD", "0.00005"))
    high_velocity = float(os.getenv("VELOCITY_HIGH_THRESHOLD", "0.0002"))
    failure_threshold = int(os.getenv("FAILURE_STREAK_THRESHOLD", "3"))
    low_time = float(os.getenv("RESPONSE_TIME_LOW_SECONDS", "15"))
    high_time = float(os.getenv("RESPONSE_TIME_HIGH_SECONDS", "40"))
    high_hints = float(os.getenv("HINTS_HIGH_THRESHOLD", "2"))
    downgrade = (
        behavior.failure_streak >= failure_threshold
        or behavior.velocity_avg < low_velocity
        or behavior.avg_response_time >= high_time
        or behavior.avg_hints_used >= high_hints
    )
    upgrade = mastery > 0.8 and behavior.velocity_avg > high_velocity and behavior.avg_response_time <= low_time
    if downgrade:
        return {"factor": -0.2, "target": _downgrade_target(base_difficulty), "reason": "struggle_indicators"}
    if upgrade:
        return {"factor": 0.2, "target": "Challenge", "reason": "high_velocity"}
    return {"factor": 0.0, "target": base_difficulty, "reason": "stable"}


def log_difficulty_shift(user: User, topic: str, base_difficulty: str, target_difficulty: str, behavior: UserTopicBehavior, mastery: float, reason: str = "behavioral_adjustment"):
    if base_difficulty == target_difficulty:
        return None
    return DifficultyShift.objects.create(
        user=user,
        topic=topic,
        from_difficulty=base_difficulty,
        to_difficulty=target_difficulty,
        reason=reason,
        mastery=mastery,
        velocity=behavior.velocity_avg,
        failure_streak=behavior.failure_streak,
        avg_response_time=behavior.avg_response_time,
        avg_hints_used=behavior.avg_hints_used,
    )


def update_shift_outcome(user: User, topic: str, mastery_before: float | None, mastery_after: float | None):
    if mastery_before is None or mastery_after is None:
        return None
    shift = DifficultyShift.objects.filter(user=user, topic=topic).order_by("-created_at").first()
    if not shift or shift.success is not None:
        return None
    if shift.to_difficulty == "Beginner":
        shift.success = mastery_after > mastery_before
    elif shift.to_difficulty == "Challenge":
        shift.success = mastery_after >= mastery_before
    else:
        shift.success = mastery_after > mastery_before
    shift.save(update_fields=["success"])
    return shift


def _rank_topics(user: User, scoring_fn):
    mastery_vector = {normalize_topic(k): float(v) for k, v in (user.mastery_vector or {}).items() if not k.startswith("_")}
    engagement = user.engagement_score or 0.5
    
    # We must only rank topics whose difficulty matches the user's assigned module difficulty.
    valid_topics = []
    profiles = list(LessonProfile.objects.all())
    lesson_ids = [str(p.lesson_id) for p in profiles if p.lesson_id]
    
    # Get the module map for these lesson IDs
    lessons = Lesson.objects.filter(id__in=lesson_ids).values("id", "module_id")
    module_by_lesson_id = {str(l["id"]): l["module_id"] for l in lessons}
    
    for profile in profiles:
        mod_id = module_by_lesson_id.get(str(profile.lesson_id))
        if not mod_id:
            continue
        # What is the user's assigned difficulty for this specific module?
        target_diff = _get_module_difficulty(user, mod_id)
        # Only consider this topic if its difficulty matches the assigned tier
        if profile.difficulty == target_diff:
            valid_topics.append(profile.topic)

    topics = set(valid_topics)
    if not topics:
        topics = set(_CANONICAL_TOPICS)
        
    candidates = []
    for topic in topics:
        mastery = float(mastery_vector.get(topic, 0.3))
        behavior = get_behavior(user, topic)
        failure_rate = recent_failure(user, topic)
        prereq_weight = prerequisite_weight(topic)
        velocity_weight = _velocity_weight(behavior.velocity_avg)
        struggle_weight = _struggle_weight(behavior)
        difficulty_adjustment = compute_difficulty_adjustment(mastery, behavior, "Beginner")
        score = scoring_fn(mastery, failure_rate, prereq_weight, engagement, difficulty_adjustment["factor"], velocity_weight, struggle_weight)
        candidates.append((score, topic, mastery, failure_rate, prereq_weight, engagement, velocity_weight, struggle_weight, difficulty_adjustment))
    candidates.sort(key=lambda item: item[0], reverse=True)
    logger.info(
        "rank_topics",
        extra={
            "user_id": user.id,
            "candidates": [
                {"topic": c[1], "score": c[0], "mastery": c[2], "failure_rate": c[3]} for c in candidates[:6]
            ],
            "mastery_vector": mastery_vector,
        },
    )
    return candidates


def _progress_user_id(user: User) -> str:
    return user.original_uuid or str(user.id)


def _normalize_track(level: str | None) -> str:
    lower = (level or "").strip().lower()
    if lower == "pro":
        return "Pro"
    if lower == "intermediate":
        return "Intermediate"
    return "Beginner"


# Mapping from recommendation canonical topics -> diagnostic quiz module keys.
# Needed because the quiz stores scores as "mod_variables_types" but the
# recommendation engine uses "variables" as the canonical topic name.
# Mapping from lesson 'module_id' -> diagnostic quiz metric keys.
# When a lesson is evaluated for difficulty, its module_id (e.g. "mod-python-basics")
# is normalized (e.g. "mod_python_basics") and mapped to the quiz keys here.
_CANONICAL_TO_MODULE_KEYS = {
    # Intro/Basics
    "mod_python_basics":       ["mod_introduction"],
    "introduction":            ["mod_introduction"],
    
    # Types/Variables
    "mod_data_types":          ["mod_variables_types"],
    "variables":               ["mod_variables_types"],
    
    # Control Flow
    "mod_control_flow":        ["mod_control_flow", "mod_loops_iteration"],
    "conditions":              ["mod_control_flow"],
    "loops":                   ["mod_loops_iteration"],
    
    # Functions
    "mod_functions":           ["mod_functions_scope"],
    "functions":               ["mod_functions_scope"],
    
    # File & Error Handling
    "mod_file_handling":       ["mod_file_handling"],
    "mod_error_handling":      ["mod_error_handling"],
    
    # OOP & Advanced
    "mod_oop":                 ["mod_oop"],
    "mod_modules_packages":    ["mod_advanced_python"],
    "mod_advanced_python":     ["mod_advanced_python"],
    "mod_real_world_projects": ["mod_real_world_projects"],
}


def _get_module_difficulty(user: User, topic: str) -> str:
    """
    Return the per-module difficulty tier stored in mastery_vector after the
    placement quiz.  Resolution order:
      1. Exact match on canonical topic key
      2. Known alias lookup via _CANONICAL_TO_MODULE_KEYS
      3. Substring search (e.g. 'loops' inside 'mod_loops_iteration')
      4. Global fallback: user.level
    """
    mastery_vector = user.mastery_vector or {}
    module_difficulty_map = mastery_vector.get("_module_difficulty") or {}

    if not module_difficulty_map:
        return _normalize_track(getattr(user, "level", None))

    canon = normalize_topic(topic)

    # 1. Exact match
    tier = module_difficulty_map.get(canon)
    if tier in ("Pro", "Intermediate", "Beginner"):
        return tier

    # 2. Known alias mapping (canonical -> module keys)
    for alias_key in _CANONICAL_TO_MODULE_KEYS.get(canon, []):
        tier = module_difficulty_map.get(alias_key)
        if tier in ("Pro", "Intermediate", "Beginner"):
            return tier

    # 3. Reverse alias: look for any stored key that maps back to canon
    for stored_key, stored_tier in module_difficulty_map.items():
        if stored_key.startswith("_"):   # skip internal keys
            continue
        # e.g. stored_key="mod_loops_iteration", canon="loops"
        if canon in stored_key or stored_key in canon:
            if stored_tier in ("Pro", "Intermediate", "Beginner"):
                return stored_tier

    # 4. Global fallback
    return _normalize_track(getattr(user, "level", None))


def _pick_next_lesson_for_topic(user: User, topic: str) -> tuple[Lesson | None, Module | None]:
    """
    Pick the earliest not-yet-completed lesson for the user within a topic,
    honouring the *per-module* difficulty tier derived from the placement quiz.

    Difficulty mapping (per module score):
      >= 75%  => 'Pro'
      >= 50%  => 'Intermediate'
      <  50%  => 'Beginner'
    """
    canon = normalize_topic(topic)
    aliases = [topic, canon]
    for k, v in _TOPIC_SYNONYMS.items():
        if k == canon:
            aliases.extend(v)
            break
    profiles = list(LessonProfile.objects.filter(topic__in=aliases).values("lesson_id", "prerequisites", "difficulty"))
    if not profiles:
        return None, None
    profile_by_lesson_id = {str(p["lesson_id"]): (p.get("prerequisites") or []) for p in profiles if p.get("lesson_id") is not None}
    lesson_ids = list(profile_by_lesson_id.keys())
    if not lesson_ids:
        return None, None

    # Fetch a sample lesson to determine its module_id for difficulty lookup
    sample_lesson = Lesson.objects.filter(id__in=lesson_ids).first()
    if sample_lesson and sample_lesson.module_id:
        target = _get_module_difficulty(user, sample_lesson.module_id)
    else:
        # Fallback to topic name if no lesson is found
        target = _get_module_difficulty(user, topic)

    lessons_qs = Lesson.objects.filter(id__in=lesson_ids, difficulty=target).order_by("module_id", "order", "id")
    if not lessons_qs.exists():
        # Graceful fallback: try all difficulties for this topic
        lessons_qs = Lesson.objects.filter(id__in=lesson_ids).order_by("module_id", "order", "id")
    lessons = list(lessons_qs[:200])
    if not lessons:
        return None, None

    user_id = _progress_user_id(user)
    completed_ids = set(
        UserProgress.objects.filter(user_id=user_id, lesson_id__in=[l.id for l in lessons], completed=True)
        .values_list("lesson_id", flat=True)
    )

    def prereqs_met(lesson_id: str) -> bool:
        raw = profile_by_lesson_id.get(str(lesson_id), []) or []
        prereq_ids = []
        for val in raw:
            try:
                prereq_ids.append(str(val))
            except Exception:
                continue
        return (not prereq_ids) or all(pid in completed_ids for pid in prereq_ids)

    for lesson in lessons:
        if lesson.id in completed_ids:
            continue
        if prereqs_met(lesson.id):
            module = Module.objects.filter(id=lesson.module_id).first()
            return lesson, module

    # All completed (or prerequisites block); return the first lesson as a safe fallback.
    first = lessons[0]
    return first, Module.objects.filter(id=first.module_id).first()


def recommend_next(user: User):
    assignment = get_or_assign_strategy(user)
    cache_key = f"recommendation:{user.id}:{assignment.strategy_name}"
    cached = cache.get(cache_key)
    if cached:
        log_recommendation_event(
            user=user,
            algorithm_name=cached.get("algorithm") or "strategy_a",
            recommended_lesson_id=cached.get("recommended_lesson_id"),
            recommended_topic=cached.get("next_topic"),
            confidence=cached.get("confidence_score") or 0.0,
        )
        logger.info("recommendation_cache_hit", extra={"user_id": user.id, "strategy": assignment.strategy_name})
        return cached
    algorithm = "strategy_a" if assignment.strategy_name == "A" else "strategy_b"
    scoring_fn = compute_priority_score if assignment.strategy_name == "A" else compute_priority_score_b
    candidates = _rank_topics(user, scoring_fn)
    
    lesson = None
    module = None
    # Iterate through candidates until we find a topic with an available lesson
    for c in candidates:
        score, topic, mastery, failure_rate, prereq_weight, engagement, velocity_weight, struggle_weight, difficulty_adjustment = c
        lesson, module = _pick_next_lesson_for_topic(user, topic)
        if lesson and module:
            break
    
    # If no topic has available lessons, we still need to set something from the best topic for logging
    if not lesson or not module:
        score, topic, mastery, failure_rate, prereq_weight, engagement, velocity_weight, struggle_weight, difficulty_adjustment = candidates[0]

    # Resolve the per-module difficulty that was actually used for this recommendation
    module_difficulty_assigned = _get_module_difficulty(user, lesson.module_id if lesson else topic)
    base_difficulty = None
    if lesson:
        base_difficulty = lesson.difficulty or module_difficulty_assigned

    reason = {
        "mastery": mastery,
        "recent_failure_rate": failure_rate,
        "prerequisite_dependency_weight": prereq_weight,
        "engagement_factor": engagement,
        "velocity_weight": velocity_weight,
        "struggle_weight": struggle_weight,
        "difficulty_adjustment_factor": difficulty_adjustment["factor"],
        "priority_score": score,
        "module_difficulty_assigned": module_difficulty_assigned,
    }

    base_difficulty = base_difficulty or module_difficulty_assigned or "Beginner"
    log_difficulty_shift(
        user,
        topic,
        base_difficulty,
        difficulty_adjustment["target"],
        get_behavior(user, topic),
        mastery,
        reason=difficulty_adjustment["reason"],
    )
    # Build explanations
    explanations = []
    reason_codes = []
    if mastery < 0.5:
        explanations.append(f"Low mastery in {topic} topic")
        reason_codes.append("low_mastery")
    if failure_rate > 0.3:
        explanations.append(f"Recent incorrect answers in {topic} questions")
        reason_codes.append("recent_incorrect")
    if prereq_weight > 0:
        explanations.append("This lesson is prerequisite for upcoming lessons")
        reason_codes.append("prerequisite")
    if difficulty_adjustment["factor"] < 0:
        explanations.append("Temporarily lowered difficulty to reinforce fundamentals")
        reason_codes.append("difficulty_adjust_down")
    # Explain placement-based difficulty assignments
    if module_difficulty_assigned == "Pro":
        explanations.append(f"Assigned Pro lessons — strong placement score in {topic}")
        reason_codes.append("placement_pro")
    elif module_difficulty_assigned == "Intermediate":
        explanations.append(f"Assigned Intermediate lessons — foundational score in {topic}")
        reason_codes.append("placement_intermediate")
    if velocity_weight < 0.2:
        explanations.append("Learning pace suggests focusing on fundamentals")
        reason_codes.append("low_velocity")

    result = {
        "next_module": {"id": module.id, "title": module.title} if module else None,
        "next_topic": topic,
        "difficulty_level": base_difficulty,
        "difficulty_override": difficulty_adjustment["target"] if difficulty_adjustment["target"] != base_difficulty else None,
        "reason_for_recommendation": reason,
        "confidence_score": round(0.5 + (score * 0.5), 2),
        "strategy": assignment.strategy_name,
        "algorithm": algorithm,
        "recommended_lesson_id": lesson.id if lesson else None,
        "recommended_lesson_title": lesson.title if lesson else None,
        "reasons": explanations,
        "reason_codes": reason_codes,
    }
    logger.info(
        "recommendation_scored",
        extra={
            "user_id": user.id,
            "topic": topic,
            "recommended_lesson_id": result["recommended_lesson_id"],
            "recommended_lesson_title": result["recommended_lesson_title"],
            "confidence": result["confidence_score"],
        },
    )
    # Fallback: Always return a lesson
    if not lesson or not module:
        first_module = Module.objects.filter(order=1).first()
        fallback = None
        fallback_module = None
        if first_module:
            fallback_module = first_module
            fallback = Lesson.objects.filter(module_id=first_module.id, difficulty="Beginner").order_by("order", "id").first()
            if not fallback:
                fallback = Lesson.objects.filter(module_id=first_module.id).order_by("order", "id").first()
        if fallback:
            logger.info(
                "fallback_beginner_selected",
                extra={"user_id": user.id, "lesson_id": fallback.id, "module_id": fallback_module.id if fallback_module else None},
            )
            result["next_module"] = {"id": fallback_module.id, "title": fallback_module.title} if fallback_module else None
            result["recommended_lesson_id"] = fallback.id
            result["recommended_lesson_title"] = fallback.title
            result["difficulty_level"] = fallback.difficulty or "Beginner"
            result["reasons"] = (result.get("reasons") or []) + ["Fallback to first unlocked beginner lesson in Module 1"]
            codes = set(result.get("reason_codes") or [])
            codes.add("fallback_beginner")
            result["reason_codes"] = list(codes)
            result["confidence_score"] = min(result["confidence_score"], 0.6)
        else:
            logger.warning("fallback_failed_no_lessons", extra={"user_id": user.id})
    log_recommendation_event(
        user=user,
        algorithm_name=algorithm,
        recommended_lesson_id=lesson.id if lesson else None,
        recommended_topic=topic,
        confidence=result["confidence_score"],
    )
    cache.set(cache_key, result, timeout=30)
    return result
