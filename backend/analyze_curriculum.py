import os
import sys
import django

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import Module, Lesson

modules = Module.objects.all().order_by('order')
for m in modules:
    lessons = Lesson.objects.filter(module_id=m.id, difficulty='Beginner').order_by('order')
    topics = [l.title for l in lessons]
    print(f"Module {m.order}: {m.title} - {len(topics)} topics")
    for t in topics:
        print(f"  - {t}")
    print("-" * 20)
