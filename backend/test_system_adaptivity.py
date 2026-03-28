import os
import django
import sys
from datetime import timezone

# Set up Django environment
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import User, Lesson, Module, UserProgress, UserMastery, Quiz, Question, QuizAttempt
from core.views import _lesson_ids_for_user_module, _module_completed, update_user_mastery

def test_system_adaptivity():
    print("=== System Adaptivity Test ===")
    
    # 1. Setup a fresh test user
    username = "adaptive_tester"
    User.objects.filter(username=username).delete()
    user = User.objects.create(username=username, level="Beginner")
    print(f"Created user '{username}' with initial level: {user.level}")

    # 2. Identify a Module and its topics
    # We'll use Module 1 (usually Python Basics)
    module = Module.objects.order_by('order').first()
    if not module:
        print("Error: No modules found. Please seed the database.")
        return
    
    print(f"\nTesting with Module: {module.title} (ID: {module.id})")

    # 3. Check Initial Lesson Recommendation (Beginner)
    initial_ids = _lesson_ids_for_user_module(user, module.id)
    initial_lessons = Lesson.objects.filter(id__in=initial_ids)
    initial_diffs = [l.difficulty for l in initial_lessons]
    print(f"Initial lesson difficulties for Beginner user: {initial_diffs}")
    
    if all(d == "Beginner" for d in initial_diffs):
        print("✅ SUCCESS: User correctly received Beginner lessons.")
    else:
        print("⚠️ WARNING: Some lessons were not Beginner. (Check if specific difficulties exist)")

    # 4. Check Module Quiz Locking
    is_quiz_locked = not _module_completed(user, module.id)
    print(f"Is Module Quiz locked? {is_quiz_locked} (Expected: True)")
    if is_quiz_locked:
        print("✅ SUCCESS: Module Quiz is locked for new user.")
    else:
        print("❌ FAILURE: Module Quiz should be locked.")

    # 5. Simulate Mastery Gain in a specific topic
    # Pick the first lesson's topic
    first_lesson = initial_lessons.first()
    topic = first_lesson.title
    print(f"\nSimulating 95% score on Topic: {topic}")
    
    # Update mastery for this topic
    new_mastery = update_user_mastery(user, module.id, 95, "quiz", topic=topic)
    user.refresh_from_db()
    print(f"New Mastery for {topic}: {user.mastery_vector.get(topic)}")

    # 6. Check Adapted Lesson Recommendation
    # Now that the user has mastered this topic, the system should serve "Pro" or "Advanced" version
    adapted_ids = _lesson_ids_for_user_module(user, module.id)
    adapted_lessons = {l.title: l.difficulty for l in Lesson.objects.filter(id__in=adapted_ids)}
    
    print(f"Adapted difficulties: {adapted_lessons}")
    if adapted_lessons.get(topic) in ["Pro", "Advanced", "Intermediate"]:
        print(f"✅ SUCCESS: System adapted! {topic} is now served at {adapted_lessons.get(topic)} level.")
    else:
        print(f"❌ FAILURE: System did not adapt {topic}. Stayed at {adapted_lessons.get(topic)}.")

    # 7. Complete all lessons and unlock Module Quiz
    print("\nMarking all module lessons as completed...")
    user_id = user.original_uuid or str(user.id)
    for lid in adapted_ids:
        UserProgress.objects.create(user_id=user_id, lesson_id=lid, completed=True)
    
    is_quiz_unlocked = _module_completed(user, module.id)
    print(f"Is Module Quiz unlocked? {is_quiz_unlocked} (Expected: True)")
    if is_quiz_unlocked:
        print("✅ SUCCESS: Module Quiz unlocked after completing all lessons.")
    else:
        print("❌ FAILURE: Module Quiz still locked.")

    # Cleanup
    # user.delete()
    print("\nTest completed.")

if __name__ == "__main__":
    test_system_adaptivity()
