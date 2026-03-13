"""
WSGI config for python_edition_django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import logging

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')

application = get_wsgi_application()

# Ensure the platform curriculum is seeded on startup (useful for fresh deployments)
# This runs only when the WSGI app is started (e.g., gunicorn on Render), not during manage.py migrate.
try:
    from django.core.management import call_command
    from django.db import OperationalError, ProgrammingError
    from django.contrib.auth import get_user_model
    from core.models import Lesson

# Ensure the platform curriculum is seeded on startup (useful for fresh deployments)
# This runs only when the WSGI app is started (e.g., gunicorn on Render), not during manage.py migrate.
try:
    from django.core.management import call_command
    from django.db import OperationalError, ProgrammingError, transaction
    from django.contrib.auth import get_user_model
    from django.utils.text import slugify
    from core.models import Module, Lesson, Quiz, Question, Challenge

    if not Lesson.objects.exists():
        logging.getLogger(__name__).info('No lessons found; seeding curriculum data...')

        # Seed curriculum logic adapted for runtime
        modules = [
            (1, "Python Fundamentals", "Core syntax, variables, types, I/O, and basics."),
            (2, "Control Flow", "Conditionals and boolean logic for decisions."),
            (3, "Loops", "Iteration with for/while loops and patterns."),
            (4, "Functions", "Reusable functions, parameters, returns, scope."),
            (5, "Data Structures", "Lists, tuples, sets, dicts, and patterns."),
            (6, "Object Oriented Programming", "Classes, objects, methods, inheritance."),
        ]

        lessons_by_module = {
            1: [
                ("Python Setup & First Program", "m1-1-setup", "print('Hello, Python!')"),
                ("Variables and Types", "m1-2-variables", "name = 'Alice'\nage = 20\nprint(name, age)"),
                ("Input and Output", "m1-3-io", "name = input('Name? ')\nprint('Hello', name)"),
                ("Mini Project: Greeting App", "m1-4-greeting", "# Build a small greeting app\n"),
            ],
            2: [
                ("Booleans & Comparisons", "m2-1-booleans", "x = 7\nprint(x > 3)"),
                ("if / elif / else", "m2-2-if-else", "x = 4\nif x % 2 == 0:\n    print('even')\nelse:\n    print('odd')"),
                ("Logical Operators", "m2-3-logic", "a, b = True, False\nprint(a and not b)"),
                ("Mini Project: Eligibility Checker", "m2-4-eligibility", "# Check simple eligibility rules\n"),
            ],
            3: [
                ("for Loops", "m3-1-for", "for i in range(3):\n    print(i)"),
                ("while Loops", "m3-2-while", "n = 3\nwhile n > 0:\n    print(n)\n    n -= 1"),
                ("Loop Patterns", "m3-3-patterns", "# Common iteration patterns\n"),
                ("Mini Project: Number Analyzer", "m3-4-analyzer", "# Analyze numbers in a range\n"),
            ],
            4: [
                ("Defining Functions", "m4-1-def", "def add(a, b):\n    return a + b\nprint(add(2,3))"),
                ("Parameters & Return", "m4-2-params", "def greet(name='World'):\n    return f'Hello {name}'"),
                ("Scope", "m4-3-scope", "x = 10\n\ndef f():\n    y = 3\n    return x + y\nprint(f())"),
                ("Mini Project: Utility Functions", "m4-4-utils", "# Build a few simple utilities\n"),
            ],
            5: [
                ("Lists", "m5-1-lists", "nums = [1,2,3]\nnums.append(4)\nprint(nums)"),
                ("Dictionaries", "m5-2-dicts", "scores = {'A': 90, 'B': 80}\nprint(scores['A'])"),
                ("Comprehensions", "m5-3-comp", "squares = [i*i for i in range(5)]\nprint(squares)"),
                ("Mini Project: Inventory", "m5-4-inventory", "# Track simple inventory with dicts\n"),
            ],
            6: [
                ("Classes and Objects", "m6-1-classes", "class Person:\n    def __init__(self, name):\n        self.name = name\nprint(Person('Alice').name)"),
                ("Methods", "m6-2-methods", "class Counter:\n    def __init__(self):\n        self.v = 0\n    def inc(self):\n        self.v += 1"),
                ("Inheritance", "m6-3-inherit", "class A: ...\nclass B(A): ..."),
                ("Mini Project: Bank Account", "m6-4-bank", "# Simple OOP bank account example\n"),
            ],
        }

        with transaction.atomic():
            module_map = {}
            for order, title, desc in modules:
                module, _ = Module.objects.get_or_create(
                    order=order,
                    defaults={"title": title, "description": desc, "image_url": None},
                )
                module_map[order] = module

            for m_order, lessons in lessons_by_module.items():
                module = module_map[m_order]
                for idx, (title, slug_seed, code) in enumerate(lessons, start=1):
                    slug = slugify(slug_seed)[:200]
                    Lesson.objects.get_or_create(
                        module_id=module.id,
                        slug=slug,
                        defaults={
                            "title": title,
                            "content": f"### {title}\n\n```python\n{code}\n```",
                            "order": idx,
                            "difficulty": "Beginner",
                            "duration": 20,
                        },
                    )

            # Optional: minimal quizzes/challenges for first module
            first = module_map[1]
            first_lessons = list(Lesson.objects.filter(module_id=first.id).order_by("order")[:2])
            for lesson in first_lessons:
                quiz, _ = Quiz.objects.get_or_create(lesson_id=lesson.id, title=f"Quick Check: {lesson.title}")
                Question.objects.get_or_create(
                    quiz_id=quiz.id,
                    text="What is the output of print(1+1)?",
                    defaults={
                        "type": "mcq",
                        "options": [{"text": "2", "correct": True}, {"text": "11", "correct": False}],
                        "points": 1,
                    },
                )
                Challenge.objects.get_or_create(
                    lesson_id=lesson.id,
                    title="Echo Input",
                    defaults={
                        "description": "Read a line and echo it.",
                        "initial_code": "def solve():\n    s = input().strip()\n    print(s)\n\nif __name__ == '__main__':\n    solve()",
                        "solution_code": "def solve():\n    s = input().strip()\n    print(s)\n\nif __name__ == '__main__':\n    solve()",
                        "test_cases": [{"input": "hello", "expected": "hello"}],
                        "points": 5,
                    },
                )

        logging.getLogger(__name__).info('Curriculum seeding completed.')

    # Create an admin user automatically if env vars are provided and no superuser exists.
    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        admin_username = os.environ.get('ADMIN_USERNAME')
        admin_email = os.environ.get('ADMIN_EMAIL')
        admin_password = os.environ.get('ADMIN_PASSWORD')
        if admin_username and admin_email and admin_password:
            logging.getLogger(__name__).info('Creating superuser from environment variables...')
            User.objects.create_superuser(username=admin_username, email=admin_email, password=admin_password)
            logging.getLogger(__name__).info('Superuser created: %s', admin_username)
        else:
            logging.getLogger(__name__).info('No superuser exists and ADMIN_* env vars not set; skipping superuser creation.')

except (OperationalError, ProgrammingError):
    # Database is not ready yet (migrations may be running) or not accessible.
    pass
except Exception as e:
    # Catch-all to avoid breaking the WSGI process if seeding fails.
    logging.getLogger(__name__).exception('Failed to seed curriculum data or create superuser: %s', e)


    # Create an admin user automatically if env vars are provided and no superuser exists.
    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        admin_username = os.environ.get('ADMIN_USERNAME')
        admin_email = os.environ.get('ADMIN_EMAIL')
        admin_password = os.environ.get('ADMIN_PASSWORD')
        if admin_username and admin_email and admin_password:
            logging.getLogger(__name__).info('Creating superuser from environment variables...')
            User.objects.create_superuser(username=admin_username, email=admin_email, password=admin_password)
            logging.getLogger(__name__).info('Superuser created: %s', admin_username)
        else:
            logging.getLogger(__name__).info('No superuser exists and ADMIN_* env vars not set; skipping superuser creation.')

except (OperationalError, ProgrammingError):
    # Database is not ready yet (migrations may be running) or not accessible.
    pass
except Exception as e:
    # Catch-all to avoid breaking the WSGI process if seeding fails.
    logging.getLogger(__name__).exception('Failed to seed curriculum data or create superuser: %s', e)
