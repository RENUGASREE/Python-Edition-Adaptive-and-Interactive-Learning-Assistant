"""
Check a specific user's mastery vector and module difficulty assignments.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import User

def check_user(username_or_email="admin"):
    user = User.objects.filter(username=username_or_email).first() or \
           User.objects.filter(email=username_or_email).first()
    
    if not user:
        print(f"User '{username_or_email}' not found. Available users:")
        for u in User.objects.all()[:10]:
            print(f"  - {u.username} ({u.email})")
        return
    
    print(f"User: {user.username}")
    print(f"Email: {user.email}")
    print(f"Level: {user.level}")
    print(f"Diagnostic completed: {user.diagnostic_completed}")
    print(f"Has taken quiz: {user.has_taken_quiz}")
    print()
    
    mastery = user.mastery_vector or {}
    diff_map = mastery.get("_module_difficulty", {})
    
    print("Module Difficulty Assignments:")
    if diff_map:
        for key, val in sorted(diff_map.items()):
            if not key.startswith("_"):
                print(f"  {key}: {val}")
    else:
        print("  (empty - no per-module difficulties set)")
    
    # Check what lessons would be returned for each module
    from core.models import Module, Lesson
    from core.serializers import ModuleSerializer
    
    print("\n" + "=" * 60)
    print("Expected lessons based on difficulty:")
    print("=" * 60)
    
    for module in Module.objects.all().order_by('order')[:3]:
        target = diff_map.get(module.id) or diff_map.get(module.id.replace("-", "_")) or user.level or "Beginner"
        print(f"\n{module.title}: Target = {target}")
        
        normalized = target.strip().lower()
        if normalized in ("pro", "advanced"):
            normalized = "Pro"
        elif normalized == "intermediate":
            normalized = "Intermediate"
        else:
            normalized = "Beginner"
        
        lessons = Lesson.objects.filter(module_id=module.id, difficulty=normalized).order_by('order')
        count = lessons.count()
        print(f"  Query: difficulty='{normalized}' -> {count} lessons")
        
        if count == 0:
            all_lessons = Lesson.objects.filter(module_id=module.id).order_by('order')
            print(f"  FALLBACK: Returning ALL {all_lessons.count()} lessons (mix of difficulties)")
            for l in all_lessons[:3]:
                print(f"    - [{l.difficulty}] {l.title}")

if __name__ == "__main__":
    import sys
    username = sys.argv[1] if len(sys.argv) > 1 else "admin"
    check_user(username)
