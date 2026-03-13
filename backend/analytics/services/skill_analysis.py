from typing import Dict, List, Tuple
from django.utils import timezone
from django.db import transaction
from assessments.models import AssessmentInteraction
from lessons.models import LessonProfile
from core.models import Lesson, Module, User
from .models import SkillGapAnalysis, LearningPlan


def _categorize(acc: float) -> str:
    if acc < 0.60:
        return "WEAK"
    if acc < 0.80:
        return "IMPROVING"
    return "STRONG"


@transaction.atomic
def analyze_user_skill_gaps(user: User) -> Tuple[Dict[str, float], Dict[str, str]]:
    rows = AssessmentInteraction.objects.filter(user=user)
    totals: Dict[str, int] = {}
    corrects: Dict[str, int] = {}
    for r in rows:
        topic = (r.topic or "").strip()
        if not topic:
            continue
        totals[topic] = totals.get(topic, 0) + 1
        if r.correctness:
            corrects[topic] = corrects.get(topic, 0) + 1
    accuracy_map: Dict[str, float] = {}
    status_map: Dict[str, str] = {}
    for topic, total in totals.items():
        acc = (corrects.get(topic, 0) / total) if total else 0.0
        accuracy_map[topic] = acc
        status_map[topic] = _categorize(acc)
        obj, _ = SkillGapAnalysis.objects.update_or_create(
            user=user,
            topic=topic,
            defaults={
                "accuracy": round(acc * 100, 2),
                "status": status_map[topic],
                "last_updated": timezone.now(),
            },
        )
    _generate_learning_plan(user, accuracy_map, status_map)
    return accuracy_map, status_map


def _generate_learning_plan(user: User, accuracy: Dict[str, float], status: Dict[str, str]) -> LearningPlan:
    weak_topics = [t for t, s in status.items() if s == "WEAK"]
    improving_topics = [t for t, s in status.items() if s == "IMPROVING"]
    lessons_qs = Lesson.objects.all()
    topic_to_lessons: Dict[str, List[int]] = {}
    for lp in LessonProfile.objects.filter(lesson_id__in=list(lessons_qs.values_list("id", flat=True))):
        topic = (lp.topic or "").strip()
        if not topic:
            continue
        topic_to_lessons.setdefault(topic, []).append(lp.lesson_id)
    rec_lessons: List[int] = []
    if weak_topics:
        for topic in weak_topics:
            rec_lessons.extend((topic_to_lessons.get(topic) or [])[:3])
    elif improving_topics:
        for topic in improving_topics:
            rec_lessons.extend((topic_to_lessons.get(topic) or [])[:2])
    else:
        rec_lessons.extend(list(lessons_qs.values_list("id", flat=True))[:3])
    rec_lessons = list(dict.fromkeys(rec_lessons))[:10]
    module_ids = list(Lesson.objects.filter(id__in=rec_lessons).values_list("module_id", flat=True))
    module_ids = list(dict.fromkeys(module_ids))
    reasoning_lines: List[str] = []
    for t in weak_topics:
        pct = round((accuracy.get(t, 0) or 0) * 100)
        reasoning_lines.append(f"{t} is weak ({pct}%).")
    for t in improving_topics:
        pct = round((accuracy.get(t, 0) or 0) * 100)
        reasoning_lines.append(f"{t} is improving ({pct}%).")
    reasoning = " ".join(reasoning_lines) or "Baseline plan generated."
    plan = LearningPlan.objects.create(
        user=user,
        recommended_modules=module_ids,
        recommended_lessons=rec_lessons,
        reasoning=reasoning,
    )
    return plan
