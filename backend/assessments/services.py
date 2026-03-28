"""Assessment scoring and interaction logging used by adaptive engines."""
from typing import Dict, List, Tuple
from core.models import User
from ai_engine.services import apply_bkt_update
from users.services import update_engagement
from .models import DiagnosticQuestion, AssessmentInteraction
from recommendation.services import update_behavior_from_interaction, update_topic_velocity, normalize_topic


def _difficulty_tier(weighted_score_pct: float) -> str:
    if weighted_score_pct > 0.70:
        return "Advanced"
    if weighted_score_pct > 0.35:
        return "Intermediate"
    return "Beginner"


def score_diagnostic(user: User, quiz_id: int, answers: List[Dict], violation_count: int = 0, update_user: bool = True) -> Tuple[Dict, float, float, str]:
    questions = list(DiagnosticQuestion.objects.filter(quiz_id=quiz_id))
    answer_map = {}
    for a in answers:
        try:
            q_id_val = a.get("questionId")
            if q_id_val is not None:
                answer_map[str(q_id_val)] = {
                    "selectedIndex": int(a.get("selectedIndex", -1)),
                    "isCorrect": bool(a.get("isCorrect", False)),
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

    for question in questions:
        total += 1
        total_points += int(getattr(question, "points", 1) or 1)
        canon_topic = normalize_topic(question.topic)
        module_totals[canon_topic] = module_totals.get(canon_topic, 0) + 1
        
        selected_payload = answer_map.get(str(question.id))
        
        is_correct = selected_payload.get("isCorrect") is True if selected_payload else False
        if is_correct:
            correct += 1
            correct_points += int(getattr(question, "points", 1) or 1)
            module_correct[canon_topic] = module_correct.get(canon_topic, 0) + 1
        
        AssessmentInteraction.objects.create(
            user=user,
            topic=canon_topic,
            correctness=is_correct,
            time_spent=(selected_payload.get("timeSpent") if selected_payload else 0),
            hints_used=(selected_payload.get("hintsUsed") if selected_payload else 0),
            source="diagnostic",
        )

    module_scores = {}
    for topic, total_count in module_totals.items():
        module_scores[topic] = round((module_correct.get(topic, 0) / total_count), 4)

    raw_score = round((correct / total), 4) if total else 0
    weighted = round((correct_points / total_points), 4) if total_points else 0
    tier = _difficulty_tier(weighted)

    if update_user:
        # Get all unique topics from current lessons to ensure full coverage
        from core.models import Lesson, UserMastery
        all_topics = set(Lesson.objects.values_list("title", flat=True))
        
        mastery_vector = user.mastery_vector or {}
        baseline = max(0.0, raw_score - 0.2) 
        
        for t in all_topics:
            canon_t = normalize_topic(t)
            if canon_t not in mastery_vector:
                mastery_vector[canon_t] = baseline

        # Update with actual scores
        for topic, score in module_scores.items():
            canon_topic = normalize_topic(topic)
            mastery_vector[canon_topic] = score
            
            # Use module mapping if available
            target_module = Lesson.objects.filter(module_id__icontains=topic.replace("mod-", "")).values_list("module_id", flat=True).first()
            if not target_module:
                target_module = topic # Fallback
            
            UserMastery.objects.update_or_create(
                user=user,
                module_id=target_module,
                defaults={"mastery_score": score, "last_source": "diagnostic"}
            )
            
        user.mastery_vector = mastery_vector
        user.diagnostic_completed = True
        user.has_taken_quiz = True
        user.level = tier
        user.save(update_fields=["mastery_vector", "diagnostic_completed", "has_taken_quiz", "level"])
        update_engagement(user, 0.05)
    return module_scores, raw_score, weighted, tier


def log_assessment_interaction(user: User, topic: str, correctness: bool, time_spent: float, hints_used: int, source: str):
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
