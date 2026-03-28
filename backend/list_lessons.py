#!/usr/bin/env python
import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "python_edition_django.settings")
django.setup()
from core.models import Lesson
lessons = Lesson.objects.all().order_by("id")
for l in lessons:
    print(f"{l.id}|{l.difficulty}|{l.title}|{len(l.content)}")
