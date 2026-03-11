from django.core.management.base import BaseCommand
from core.models import Challenge

CHALLENGES = [
    ("7 Day Streak Challenge", "Practice coding daily for 7 consecutive days.", "print('Day 1')", None, [], 10),
    ("30 Lessons in 30 Days", "Complete 30 lessons within 30 days.", "print('Lesson 1')", None, [], 50),
    ("Debugging Master Challenge", "Fix given buggy snippets and pass tests.", "print('Fix me')", None, [{"expected": ""}], 30),
    ("Daily Coding Habit Builder", "Solve small problems daily to build consistency.", "print('Habit')", None, [], 20),
]

class Command(BaseCommand):
    help = "Seed sample platform challenges"

    def handle(self, *args, **options):
        count = 0
        for title, description, initial_code, solution_code, test_cases, points in CHALLENGES:
            Challenge.objects.get_or_create(
                title=title,
                defaults={
                    "lesson_id": 0,
                    "description": description,
                    "initial_code": initial_code,
                    "solution_code": solution_code,
                    "test_cases": test_cases,
                    "points": points,
                }
            )
            count += 1
        self.stdout.write(self.style.SUCCESS(f"Seeded {count} sample challenges"))
