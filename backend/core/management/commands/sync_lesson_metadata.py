"""python manage.py sync_lesson_metadata -- Fix Adaptive Path Metadata"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Lesson, Module
from lessons.models import LessonProfile

class Command(BaseCommand):
    help = "Sync LessonProfile metadata for all lessons to enable adaptive paths"

    def handle(self, *args, **options):
        self.stdout.write("🔄 Syncing LessonProfile metadata for adaptive routing...")
        
        lessons = Lesson.objects.all().order_by('module_id', 'order')
        created_count = 0
        updated_count = 0

        with transaction.atomic():
            for lesson in lessons:
                # Find previous lesson in same module for prerequisite
                prev_lesson = Lesson.objects.filter(
                    module_id=lesson.module_id,
                    order=lesson.order - 1
                ).first()
                
                prereqs = [prev_lesson.id] if prev_lesson else []
                
                profile, created = LessonProfile.objects.update_or_create(
                    lesson_id=lesson.id,
                    defaults={
                        "topic": lesson.title,
                        "difficulty": lesson.difficulty or "Beginner",
                        "prerequisites": prereqs,
                    }
                )
                
                if created:
                    created_count += 1
                else:
                    updated_count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Success: Created {created_count}, Updated {updated_count} lesson profiles."))
