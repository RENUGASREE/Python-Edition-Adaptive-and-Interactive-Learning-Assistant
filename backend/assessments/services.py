"""Assessment scoring and interaction logging used by adaptive engines."""
from typing import Dict, List, Tuple
from core.models import User
from core.adaptive import QUIZ_TOPIC_MODULE_MAP, difficulty_for_score, normalize_level, normalize_topic
from ai_engine.services import apply_bkt_update
from users.services import update_engagement
from .models import DiagnosticQuestion, AssessmentInteraction


def _difficulty_tier(weighted_score_pct: float) -> str:
    """Global tier based on overall weighted score."""
    return difficulty_for_score(weighted_score_pct)


def _module_difficulty_tier(module_score: float) -> str:
    return difficulty_for_score(module_score)


def score_diagnostic(user: User, quiz_id: int, answers: List[Dict], violation_count: int = 0, update_user: bool = True) -> Tuple[Dict, float, float, str]:
    questions = list(DiagnosticQuestion.objects.filter(quiz_id=quiz_id).prefetch_related("choices"))
    answer_map = {}
    for a in answers:
        try:
            q_id_val = a.get("questionId")
            if q_id_val is not None:
                answer_map[str(q_id_val)] = {
                    "selectedIndex": int(a.get("selectedIndex", -1)),
                    "selectedOptionId": a.get("selectedOptionId"),
                    "timeSpent": float(a.get("timeSpent", 0)),
                    "hintsUsed": int(a.get("hintsUsed", 0)),
                }
        except (ValueError, TypeError):
            continue

    module_totals = {}
    module_correct = {}
    total = 0
    correct = 0
    total_points = 0
    correct_points = 0
    interactions = []

    for question in questions:
        total += 1
        total_points += int(getattr(question, "points", 1) or 1)
        canon_topic = normalize_topic(question.topic)
        module_totals[canon_topic] = module_totals.get(canon_topic, 0) + 1

        selected_payload = answer_map.get(str(question.id))
        selected_option_id = str(selected_payload.get("selectedOptionId")) if selected_payload and selected_payload.get("selectedOptionId") is not None else None
        is_correct = False
        if selected_payload:
            # Try to match the option ID first (robust)
            if question.choices.exists():
                is_correct = any(str(choice.id) == selected_option_id and choice.is_correct for choice in question.choices.all())
                
            # Fallback: If ID didn't match or question has no choice objects, check the index
            if not is_correct:
                raw_index = selected_payload.get("selectedIndex", -1)
                is_correct = raw_index == int(question.correct_index)

        if is_correct:
            correct += 1
            correct_points += int(getattr(question, "points", 1) or 1)
            module_correct[canon_topic] = module_correct.get(canon_topic, 0) + 1

        interactions.append(
            AssessmentInteraction(
                user=user,
                topic=canon_topic,
                correctness=is_correct,
                time_spent=(selected_payload.get("timeSpent") if selected_payload else 0),
                hints_used=(selected_payload.get("hintsUsed") if selected_payload else 0),
                source="diagnostic",
            )
        )

    if interactions:
        AssessmentInteraction.objects.bulk_create(interactions)

    module_scores = {}
    for topic, total_count in module_totals.items():
        module_scores[topic] = round((module_correct.get(topic, 0) / total_count), 4)

    raw_score = round((correct / total), 4) if total else 0
    weighted = round((correct_points / total_points), 4) if total_points else 0
    tier = _difficulty_tier(weighted)

    if update_user:
        from core.models import Lesson, UserMastery
        all_topics = set(Lesson.objects.values_list("title", flat=True))

        mastery_vector = user.mastery_vector or {}
        baseline = max(0.0, raw_score - 0.2)

        for t in all_topics:
            canon_t = normalize_topic(t)
            if canon_t not in mastery_vector:
                mastery_vector[canon_t] = baseline

        # Build per-module difficulty map based on individual module scores
        module_difficulty_map = mastery_vector.get("_module_difficulty") or {}

        for topic, score in module_scores.items():
            canon_topic = normalize_topic(topic)
            mastery_vector[canon_topic] = score
            mastery_vector[canon_topic.replace("_", "-")] = score

            # Assign per-module difficulty tier
            module_difficulty = _module_difficulty_tier(score)

            # Ensure we check both dash and underscore versions in the mapping
            target_module = QUIZ_TOPIC_MODULE_MAP.get(canon_topic) or \
                           QUIZ_TOPIC_MODULE_MAP.get(canon_topic.replace("_", "-")) or \
                           canon_topic

            module_difficulty_map[target_module] = module_difficulty
            module_difficulty_map[target_module.replace("-", "_")] = module_difficulty
            module_difficulty_map[target_module.replace("_", "-")] = module_difficulty

            UserMastery.objects.update_or_create(
                user=user,
                module_id=target_module,
                defaults={"mastery_score": score, "last_source": "diagnostic"},
            )

        # Persist the per-module difficulty map inside mastery_vector
        mastery_vector["_module_difficulty"] = module_difficulty_map

        user.mastery_vector = mastery_vector
        user.diagnostic_completed = True
        user.has_taken_quiz = True
        # Global level is strictly based on the overall weighted score across all modules.
        # Each module gets its OWN difficulty tier from module_difficulty_map — not this global level.
        user.level = normalize_level(tier)
        user.save(update_fields=["mastery_vector", "diagnostic_completed", "has_taken_quiz", "level"])
        update_engagement(user, 0.05)
    return module_scores, raw_score, weighted, tier


def log_assessment_interaction(user: User, topic: str, correctness: bool, time_spent: float, hints_used: int, source: str):
    from recommendation.services import update_behavior_from_interaction, update_topic_velocity
    
    AssessmentInteraction.objects.create(
        user=user,
        topic=topic,
        correctness=correctness,
        time_spent=time_spent,
        hints_used=hints_used,
        source=source,
    )
    update_behavior_from_interaction(user, topic, correctness, float(time_spent or 0), int(hints_used or 0))
    new_mastery = apply_bkt_update(user, topic, correctness)
    update_topic_velocity(user, topic, new_mastery)
    return new_mastery
