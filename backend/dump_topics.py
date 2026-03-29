import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()
from lessons.models import LessonProfile

with open('db_topics.txt', 'w', encoding='utf-8') as f:
    topics = set(LessonProfile.objects.values_list('topic', flat=True))
    f.write("\n".join(sorted(topics)))
