import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "python_edition_django.settings")
django.setup()

from django.contrib.auth import get_user_model
from analytics.analytics_services import mastery_progression
from core.models import Module, Lesson, Challenge

User = get_user_model()
user = User.objects.first()

print("User:", user.username)

mp = mastery_progression(user)
print(f"Mastery Progression length: {len(mp)}")
if mp:
    print("First item:", mp[0])

modules = Module.objects.all()
print(f"Modules count: {modules.count()}")
for m in modules[:2]:
    lessons = Lesson.objects.filter(module_id=m.id)
    print(f"Module {m.title}: {lessons.count()} lessons")
    for l in lessons[:1]:
        print(f"  Lesson: {l.title}, unloc={getattr(l, 'unlocked', 'None')}")
        ch = Challenge.objects.filter(lesson_id=l.id).first()
        if ch:
            print(f"    Challenge: {ch.title}")
