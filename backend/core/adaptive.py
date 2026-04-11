from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from django.core.cache import cache

from core.models import Lesson, QuizAttempt, UserProgress, UserMastery


MODULE_ALIAS_MAP = {
    "mod-introduction": "mod-python-basics",
    "mod_introduction": "mod-python-basics",
    "mod-variables-types": "mod-data-types",
    "mod_variables_types": "mod-data-types",
    "mod-control-flow": "mod-control-flow",
    "mod_control_flow": "mod-control-flow",
    "mod-loops-iteration": "mod-loops-iteration",
    "mod_loops_iteration": "mod-loops-iteration",
    "mod-functions-scope": "mod-functions",
    "mod_functions_scope": "mod-functions",
    "mod-file-handling": "mod-modules-packages",
    "mod_file_handling": "mod-modules-packages",
    "mod-error-handling": "mod-modules-packages",
    "mod_error_handling": "mod-modules-packages",
}


QUIZ_TOPIC_MODULE_MAP = {
    "mod-introduction": "mod-python-basics",
    "mod-variables-types": "mod-data-types",
    "mod-control-flow": "mod-control-flow",
    "mod-loops-iteration": "mod-loops-iteration",
    "mod-functions-scope": "mod-functions",
    "mod-file-handling": "mod-modules-packages",
    "mod-error-handling": "mod-modules-packages",
}


def normalize_level(level: str | None) -> str:
    lower = (level or "").strip().lower()
    if lower in {"pro", "advanced"}:
        return "Pro"
    if lower == "intermediate":
        return "Intermediate"
    return "Beginner"


def difficulty_for_score(score: float) -> str:
    value = float(score)
    if value > 1:
        value = value / 100
    value = max(0.0, min(1.0, value))
    if value < 0.40:
        return "Beginner"
    if value < 0.75:
        return "Intermediate"
    return "Pro"


def progress_user_id(user) -> str:
    return user.original_uuid or str(user.id)


def canonical_module_id(module_id: str | None) -> str | None:
    if module_id is None:
        return None
    raw = str(module_id)
    return MODULE_ALIAS_MAP.get(raw, raw.replace("_", "-"))


def module_lookup_keys(module_id: str | None) -> list[str]:
    canonical = canonical_module_id(module_id)
    if not canonical:
        return []
    keys = {canonical, canonical.replace("-", "_")}
    for alias, target in MODULE_ALIAS_MAP.items():
        if target == canonical:
            keys.add(alias)
            keys.add(alias.replace("-", "_"))
    return list(keys)


def get_module_difficulty_map(user) -> dict[str, str]:
    mastery_vector = user.mastery_vector or {}
    difficulty_map = dict(mastery_vector.get("_module_difficulty", {}) or {})
    normalized: dict[str, str] = {}

    for key, value in difficulty_map.items():
        level = normalize_level(value)
        for lookup_key in module_lookup_keys(key):
            normalized[lookup_key] = level

    attempts = QuizAttempt.objects.filter(user=user).only("notes").order_by("completed_at")
    for attempt in attempts:
        notes = attempt.notes or ""
        if "module:" not in notes or ":level:" not in notes:
            continue
        try:
            module_part = notes.split("module:", 1)[1].split(":level:", 1)[0]
            level_part = notes.split(":level:", 1)[1].split(":", 1)[0]
        except IndexError:
            continue
        level = normalize_level(level_part)
        for lookup_key in module_lookup_keys(module_part):
            normalized[lookup_key] = level

    return normalized


def get_user_module_difficulty(user, module_id: str, default: str | None = None) -> str:
    difficulty_map = get_module_difficulty_map(user)
    for key in module_lookup_keys(module_id):
        if key in difficulty_map:
            return difficulty_map[key]
    return normalize_level(default or getattr(user, "level", None))


def update_user_module_mastery(user, module_id: str, score: float, source: str) -> float:
    canonical_id = canonical_module_id(module_id) or str(module_id)
    normalized_score = float(score)
    if normalized_score > 1:
        normalized_score = normalized_score / 100
    normalized_score = max(0.0, min(1.0, normalized_score))

    mastery, created = UserMastery.objects.get_or_create(
        user=user,
        module_id=canonical_id,
        defaults={"mastery_score": normalized_score, "last_source": source},
    )
    if not created:
        mastery.mastery_score = round((mastery.mastery_score * 0.7) + (normalized_score * 0.3), 4)
        mastery.last_source = source
        mastery.save(update_fields=["mastery_score", "last_source", "last_updated"])

    mastery_vector = dict(user.mastery_vector or {})
    difficulty_map = dict(mastery_vector.get("_module_difficulty", {}) or {})
    difficulty = difficulty_for_score(mastery.mastery_score)

    mastery_vector[canonical_id] = mastery.mastery_score
    for key in module_lookup_keys(canonical_id):
        difficulty_map[key] = difficulty

    mastery_vector["_module_difficulty"] = difficulty_map
    user.mastery_vector = mastery_vector
    user.save(update_fields=["mastery_vector"])
    return mastery.mastery_score


def lesson_queryset_for_user_module(user, module_id: str):
    difficulty = get_user_module_difficulty(user, module_id)
    lessons = Lesson.objects.filter(module_id=module_id, difficulty=difficulty).order_by("order", "id")
    if lessons.exists():
        return lessons
    return Lesson.objects.filter(module_id=module_id).order_by("order", "id")


def lesson_ids_for_user_module(user, module_id: str) -> list[str]:
    return list(lesson_queryset_for_user_module(user, module_id).values_list("id", flat=True))


def group_lessons_for_modules(module_ids: Iterable[str]) -> dict[str, list[Lesson]]:
    grouped: dict[str, list[Lesson]] = defaultdict(list)
    for lesson in Lesson.objects.filter(module_id__in=list(module_ids)).order_by("module_id", "order", "id"):
        grouped[str(lesson.module_id)].append(lesson)
    return grouped


def bump_user_cache_version(user) -> int:
    key = f"user-cache-version:{user.id}"
    version = cache.get(key, 1)
    try:
        version = int(version) + 1
    except (TypeError, ValueError):
        version = 2
    cache.set(key, version, timeout=None)
    return version


def get_user_cache_version(user) -> int:
    key = f"user-cache-version:{user.id}"
    version = cache.get(key)
    if version is None:
        cache.set(key, 1, timeout=None)
        return 1
    return int(version)


def cache_key_for_user(user, *parts: object) -> str:
    version = get_user_cache_version(user)
    safe_parts = ":".join(str(part) for part in parts)
    return f"user-cache:{user.id}:v{version}:{safe_parts}"
