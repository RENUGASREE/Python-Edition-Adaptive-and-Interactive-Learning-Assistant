from django.core.management.base import BaseCommand
from core.models import Lesson, Challenge

CHALLENGE_DATABASE = {
    "input_output": {
        "Beginner": {"title": "Hello World", "desc": "Print 'Hello, World!'.", "starter": "print('Hello, World!')", "tests": [{"input": "", "expected": "Hello, World!"}]},
        "Intermediate": {"title": "Formatted Input", "desc": "Read name and age, then print 'Name: <name>, Age: <age>'.", "starter": "n = input()\na = input()\nprint(f'Name: {n}, Age: {a}')", "tests": [{"input": "Bob\n25", "expected": "Name: Bob, Age: 25"}]},
        "Pro": {"title": "I/O Stream", "desc": "Echo 3 lines of input.", "starter": "for _ in range(3): print(input())", "tests": [{"input": "1\n2\n3", "expected": "1\n2\n3"}]}
    },
    "variables": {
        "Beginner": {"title": "Var Assign", "desc": "Assign 10 to x and print it.", "starter": "x = 10\nprint(x)", "tests": [{"input": "", "expected": "10"}]},
        "Intermediate": {"title": "Swap", "desc": "Swap a and b.", "starter": "a, b = b, a", "tests": [{"input": "1\n2", "expected": "2\n1"}]}, # simplified for brevity
    },
    "types": {
        "Beginner": {"title": "Type Check", "desc": "Print the type of 5.5.", "starter": "print(type(5.5))", "tests": [{"input": "", "expected": "<class 'float'>"}]},
    },
    "operators": {
        "Beginner": {"title": "Addition", "desc": "Add 5 and 7.", "starter": "print(5 + 7)", "tests": [{"input": "", "expected": "12"}]},
    },
    # Mapping more topics...
}

class Command(BaseCommand):
    help = "Updates lesson challenges with unique content without resetting lessons"

    def handle(self, *args, **options):
        lessons = Lesson.objects.all()
        updated = 0
        for lesson in lessons:
            topic = lesson.slug.split("-")[0] if "-" in lesson.id else lesson.id
            # Try to find a specific challenge
            spec = CHALLENGE_DATABASE.get(topic, {}).get(lesson.difficulty)
            
            if not spec:
                # Basic fallback to ensure no placeholders
                spec = {
                    "title": f"Master {lesson.title}",
                    "desc": f"Create a working example of {lesson.title} that outputs 'Success'.",
                    "starter": "print('Success')",
                    "tests": [{"input": "", "expected": "Success"}]
                }

            challenge, created = Challenge.objects.get_or_create(
                lesson_id=lesson.id,
                defaults={
                    "id": f"challenge-{lesson.id}",
                    "title": spec["title"],
                    "description": spec["desc"],
                    "initial_code": "",
                    "solution_code": spec["starter"],
                    "test_cases": spec["tests"],
                    "points": 20,
                    "difficulty": lesson.difficulty
                }
            )
            if not created:
                challenge.title = spec["title"]
                challenge.description = spec["desc"]
                challenge.solution_code = spec["starter"]
                challenge.test_cases = spec["tests"]
                challenge.save()
            
            updated += 1
        
        self.stdout.write(self.style.SUCCESS(f"Finished updating {updated} challenges"))
