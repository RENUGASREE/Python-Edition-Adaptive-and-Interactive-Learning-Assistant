"""
Diagnose why all modules still show Beginner.
Checks:
1. What difficulty values actually exist in the lessons table
2. What _module_difficulty map is stored in mastery_vector for each user
3. Whether lesson difficulty values match what the engine expects
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import User, Lesson
from assessments.models import DiagnosticQuizAttempt
from recommendation.services import _get_module_difficulty, normalize_topic

# 1. What difficulty values exist in the lessons table?
print("=" * 60)
print("1. DISTINCT DIFFICULTY VALUES IN lessons TABLE")
print("=" * 60)
difficulties = Lesson.objects.values_list("difficulty", flat=True).distinct()
for d in sorted(set(difficulties)):
    count = Lesson.objects.filter(difficulty=d).count()
    print(f"  '{d}' -> {count} lessons")

# 2. Check mastery_vector _module_difficulty for all users
print("\n" + "=" * 60)
print("2. mastery_vector['_module_difficulty'] per user")
print("=" * 60)
for user in User.objects.all():
    mv = user.mastery_vector or {}
    md_map = mv.get("_module_difficulty", {})
    print(f"\n  User: {user.username} | Global level: {user.level}")
    if not md_map:
        print("  *** _module_difficulty is EMPTY / MISSING ***")
    else:
        for topic, tier in md_map.items():
            resolved = _get_module_difficulty(user, topic)
            print(f"    {topic:<35} stored={tier:<14} resolved={resolved}")

# 3. For a user, show what lessons would be found per topic and difficulty
print("\n" + "=" * 60)
print("3. LESSON AVAILABILITY PER TOPIC + DIFFICULTY TARGET")
print("=" * 60)
for user in User.objects.all():
    mv = user.mastery_vector or {}
    md_map = mv.get("_module_difficulty", {})
    if not md_map:
        continue
    print(f"\n  User: {user.username}")
    for topic, tier in md_map.items():
        matching = Lesson.objects.filter(difficulty=tier).count()
        any_lessons = Lesson.objects.filter(
            module_id__icontains=topic.replace("mod_", "").replace("_", "-")
        ).count()
        print(f"    {topic:<35} target={tier:<14} lessons_with_this_difficulty={matching}  lessons_in_module={any_lessons}")

print("\nDiagnosis complete.")
