import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import User, Lesson, UserProgress
from lessons.models import LessonProfile
from recommendation.services import _rank_topics, compute_priority_score, _pick_next_lesson_for_topic, normalize_topic, _CANONICAL_TO_MODULE_KEYS, _get_module_difficulty

user = User.objects.get(email='editionpython@gmail.com')
score, topic, mastery, failure_rate, prereq_weight, engagement, velocity_weight, struggle_weight, difficulty_adjustment = _rank_topics(user, compute_priority_score)

print(f"Top ranked topic: {topic}")
target_diff = _get_module_difficulty(user, topic)
print(f"Target difficulty for {topic}: {target_diff}")

# What aliases does this topic have?
canon = normalize_topic(topic)
from recommendation.services import _TOPIC_SYNONYMS
aliases = [canon]
for k, v in _TOPIC_SYNONYMS.items():
    if k == canon:
        aliases = [canon] + v
        break

print(f"Aliases for {topic}: {aliases}")
profiles = list(LessonProfile.objects.filter(topic__in=aliases).values("lesson_id", "prerequisites", "difficulty"))
print(f"Found {len(profiles)} LessonProfiles for these aliases")

lesson_ids = [p["lesson_id"] for p in profiles if p.get("lesson_id") is not None]
qs = Lesson.objects.filter(id__in=lesson_ids)
print(f"Found {qs.count()} actual Lessons in DB matching these IDs")
for L in qs:
    print(f"  Lesson: {L.id} - {L.title} (difficulty={L.difficulty})")
