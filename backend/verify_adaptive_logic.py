import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import User, Lesson
from core.views import _lesson_ids_for_user_module

def test_adaptive_logic():
    print("Verifying Adaptive Logic...")
    
    # Setup test users
    u_pro, _ = User.objects.get_or_create(username="test_pro", defaults={"level": "Advanced"})
    u_beg, _ = User.objects.get_or_create(username="test_beg", defaults={"level": "Beginner"})
    
    # Get a lesson from Module 1
    m1_lessons = Lesson.objects.filter(module_id__order=1)
    if not m1_lessons.exists():
        print("Error: No lessons found in Module 1. Please run populate_pro_curriculum.py first.")
        return
        
    m1_id = m1_lessons.first().module_id
    
    # Check Pro User
    pro_ids = _lesson_ids_for_user_module(u_pro, m1_id)
    pro_lessons = Lesson.objects.filter(id__in=pro_ids)
    pro_diffs = set(l.difficulty for l in pro_lessons)
    print(f"Pro User ({u_pro.level}) received lessons with difficulties: {pro_diffs}")
    
    # Check Beginner User
    beg_ids = _lesson_ids_for_user_module(u_beg, m1_id)
    beg_lessons = Lesson.objects.filter(id__in=beg_ids)
    beg_diffs = set(l.difficulty for l in beg_lessons)
    print(f"Beginner User ({u_beg.level}) received lessons with difficulties: {beg_diffs}")

    # Final Check
    if "Pro" in pro_diffs and "Beginner" in beg_diffs:
        print("\nSUCCESS: Logic verified. Pro users get Pro content, Beginner users get Beginner content.")
    else:
        print("\nFAILURE: Logic mismatch detected.")

if __name__ == "__main__":
    test_adaptive_logic()
