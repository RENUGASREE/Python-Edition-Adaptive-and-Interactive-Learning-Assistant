"""
Diagnostic script to check lesson difficulties in the database.
Run this to verify what lessons exist for each difficulty level.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import Module, Lesson
from collections import defaultdict

def check_lessons():
    print("=" * 60)
    print("LESSON DIFFICULTY DIAGNOSTIC")
    print("=" * 60)
    
    modules = Module.objects.all().order_by('order')
    
    for module in modules:
        lessons = Lesson.objects.filter(module_id=module.id).order_by('order', 'difficulty')
        if not lessons:
            print(f"\n{module.title} ({module.id}): NO LESSONS")
            continue
            
        by_difficulty = defaultdict(list)
        for lesson in lessons:
            by_difficulty[lesson.difficulty or "Unknown"].append(lesson.title)
        
        print(f"\n{module.title} ({module.id}):")
        for diff, titles in sorted(by_difficulty.items()):
            print(f"  [{diff}]: {len(titles)} lessons")
            for t in titles[:3]:  # Show first 3
                print(f"    - {t}")
            if len(titles) > 3:
                print(f"    ... and {len(titles) - 3} more")
    
    print("\n" + "=" * 60)
    print("SUMMARY: Pro lessons exist?")
    print("=" * 60)
    
    for module in modules:
        has_pro = Lesson.objects.filter(module_id=module.id, difficulty="Pro").exists()
        has_advanced = Lesson.objects.filter(module_id=module.id, difficulty="Advanced").exists()
        status = "OK (Pro)" if has_pro else ("OK (Advanced)" if has_advanced else "MISSING PRO!")
        print(f"{module.title}: {status}")

if __name__ == "__main__":
    check_lessons()
