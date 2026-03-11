from django.core.management.base import BaseCommand
from gamification.models import Badge

BADGES = [
    ("first-steps", "First Steps – Complete first lesson"),
    ("quiz-master", "Quiz Master – Score 80%+ in placement quiz"),
    ("consistency-starter", "Consistency Starter – 3 day streak"),
    ("code-warrior", "Code Warrior – Complete 10 lessons"),
    ("python-apprentice", "Python Apprentice – Complete Module 1"),
    ("python-expert", "Python Expert – Complete all modules"),
    ("perfect-score", "Perfect Score – 100% on any quiz"),
    ("fast-learner", "Fast Learner – Finish module in under 3 days"),
]

class Command(BaseCommand):
    help = "Seed sample badges"

    def handle(self, *args, **options):
        created = 0
        for code, title in BADGES:
            obj, was_created = Badge.objects.get_or_create(code=code, defaults={"title": title, "description": title})
            if not was_created:
                obj.title = title
                obj.description = title
                obj.save(update_fields=["title", "description"])
            created += 1
        self.stdout.write(self.style.SUCCESS(f"Seeded/updated {created} badges"))
