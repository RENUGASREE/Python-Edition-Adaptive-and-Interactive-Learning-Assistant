import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()
from core.models import Lesson

with open('file_handling_lessons_utf8.txt', 'w', encoding='utf-8') as f:
    f.write('Lessons for all modules:\n')
    for module_id in Lesson.objects.values_list('module_id', flat=True).distinct():
        f.write(f"\nMODULE: {module_id}\n")
        for L in Lesson.objects.filter(module_id=module_id):
            f.write(f' - [ID: {L.id}] {L.title} | {L.difficulty}\n')
