from django.core.management.base import BaseCommand
from core.models import UserProgress, Lesson
import logging

class Command(BaseCommand):
    help = "Migrate legacy lesson IDs in UserProgress to current IDs"

    def handle(self, *args, **options):
        # Mapping pattern: les-python-basics-{n}-{difficulty} 
        # to m1-{n}-{something}-{difficulty}-{difficulty}
        
        all_lessons = list(Lesson.objects.all())
        lesson_map = {}
        
        # Build a map based on order and difficulty
        for l in all_lessons:
            # We assume m1 lessons are the target
            if l.id.startswith("m1-"):
                # key e.g. (1, 'beginner')
                # Note: difficulty in Lesson table is capitalized or lowercase?
                # Based on check: 'Beginner', 'Intermediate', 'Pro'
                key = (l.order, l.difficulty.lower())
                lesson_map[key] = l.id
        
        self.stdout.write(f"Built map for {len(lesson_map)} target lessons.")
        
        progress_records = UserProgress.objects.all()
        updated_count = 0
        
        for p in progress_records:
            old_id = p.lesson_id
            if old_id.startswith("les-python-basics-"):
                # Format: les-python-basics-1-pro
                parts = old_id.split('-')
                if len(parts) >= 5:
                    try:
                        order = int(parts[3])
                        diff = parts[4].lower()
                        new_id = lesson_map.get((order, diff))
                        
                        if new_id:
                            p.lesson_id = new_id
                            p.save()
                            updated_count += 1
                            self.stdout.write(f"Updated: {old_id} -> {new_id}")
                        else:
                            self.stdout.write(self.style.WARNING(f"No match for {old_id} (order={order}, diff={diff})"))
                    except ValueError:
                        self.stdout.write(self.style.ERROR(f"Failed to parse ID: {old_id}"))
        
        self.stdout.write(self.style.SUCCESS(f"Successfully migrated {updated_count} progress records."))
