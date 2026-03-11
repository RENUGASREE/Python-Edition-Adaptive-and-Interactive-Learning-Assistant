from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify

from core.models import Module, Lesson, Quiz, Question, Challenge
from lessons.models import LessonProfile


MODULE_SPECS = [
    (1, "Introduction to Python", "Get started with Python syntax, variables, and basic input/output."),
    (2, "Control Flow", "Make decisions with if/elif/else and write logical conditions."),
    (3, "Loops & Iteration", "Repeat tasks efficiently with for/while loops and iteration patterns."),
    (4, "Data Structures", "Work with lists, tuples, sets, and dictionaries effectively."),
    (5, "Functions & Scope", "Write reusable functions and understand scope and parameters."),
    (6, "Object Oriented Programming", "Model real-world problems using classes, objects, and inheritance."),
]

OOP_LESSONS = [
    (1, "Classes and Objects", "classes-objects"),
    (2, "Attributes and Methods", "attributes-methods"),
    (3, "Constructors and __init__", "constructors-init"),
    (4, "Inheritance", "inheritance"),
    (5, "Encapsulation and Polymorphism", "encapsulation-polymorphism"),
]

DIFFICULTIES = ["Beginner", "Intermediate", "Pro"]


def _lesson_content(title: str, difficulty: str) -> str:
    level_note = {
        "Beginner": "Focus on the core idea and small examples.",
        "Intermediate": "Add edge cases and common mistakes to avoid.",
        "Pro": "Go deeper with patterns, trade-offs, and design choices.",
    }.get(difficulty, "Practice with a small example.")
    return "\n\n".join([
        f"## {title}",
        level_note,
        "### Example",
        "```python\n# Write a small example here\n```\n",
        "### Quick exercise",
        "- Modify the example and explain what changed.",
    ])


def _quiz_questions_for(title: str):
    base = title.strip()
    return [
        {
            "text": f"In Python OOP, what best describes the purpose of {base.lower()}?",
            "options": [
                {"text": "A concept used to model behavior and data together", "correct": True},
                {"text": "A built-in loop construct", "correct": False},
                {"text": "A database table definition", "correct": False},
                {"text": "A syntax rule for importing modules", "correct": False},
            ],
            "points": 2,
        },
        {
            "text": "Which statement is true about instance attributes?",
            "options": [
                {"text": "They are stored per-object and can differ between instances", "correct": True},
                {"text": "They must be declared with var/let", "correct": False},
                {"text": "They exist only inside loops", "correct": False},
                {"text": "They cannot be changed after assignment", "correct": False},
            ],
            "points": 2,
        },
        {
            "text": "What is the role of `__init__` in a class?",
            "options": [
                {"text": "It initializes a new object instance", "correct": True},
                {"text": "It deletes an object instance", "correct": False},
                {"text": "It imports required modules", "correct": False},
                {"text": "It compiles Python code to bytecode", "correct": False},
            ],
            "points": 2,
        },
        {
            "text": "Inheritance is mainly used to:",
            "options": [
                {"text": "Reuse and extend behavior from an existing class", "correct": True},
                {"text": "Speed up Python execution", "correct": False},
                {"text": "Replace the need for functions", "correct": False},
                {"text": "Prevent creating objects", "correct": False},
            ],
            "points": 2,
        },
        {
            "text": "Encapsulation encourages you to:",
            "options": [
                {"text": "Hide implementation details behind a clean interface", "correct": True},
                {"text": "Avoid using classes entirely", "correct": False},
                {"text": "Store everything in global variables", "correct": False},
                {"text": "Only use static methods", "correct": False},
            ],
            "points": 2,
        },
        {
            "text": "Polymorphism allows:",
            "options": [
                {"text": "Different objects to be used through the same interface", "correct": True},
                {"text": "Only one method name in a program", "correct": False},
                {"text": "A list to hold only one data type", "correct": False},
                {"text": "A class to have no methods", "correct": False},
            ],
            "points": 2,
        },
    ]


class Command(BaseCommand):
    help = "Seed core curriculum (modules/lessons/quizzes/questions/challenges) and LessonProfiles. Safe to run multiple times."

    def handle(self, *args, **options):
        created_modules = 0
        created_lessons = 0
        created_quizzes = 0
        created_questions = 0
        created_challenges = 0
        upserted_profiles = 0

        with transaction.atomic():
            # Modules (ensure order 1..6 exists)
            module_by_order = {}
            for order, title, description in MODULE_SPECS:
                module, created = Module.objects.get_or_create(
                    order=order,
                    defaults={"title": title, "description": description, "image_url": None},
                )
                if not created:
                    needs_update = (module.title != title) or (module.description != description)
                    if needs_update:
                        module.title = title
                        module.description = description
                        module.save(update_fields=["title", "description"])
                else:
                    created_modules += 1
                module_by_order[order] = module

            # Add Module 6 lessons (OOP) across Beginner/Intermediate/Pro
            oop_module = module_by_order[6]
            for difficulty in DIFFICULTIES:
                for order, title, slug in OOP_LESSONS:
                    lesson, created = Lesson.objects.get_or_create(
                        module_id=oop_module.id,
                        difficulty=difficulty,
                        slug=slugify(slug),
                        defaults={
                            "title": title,
                            "content": _lesson_content(title, difficulty),
                            "order": order,
                            "duration": 20 if difficulty == "Beginner" else 30 if difficulty == "Intermediate" else 40,
                        },
                    )
                    if not created:
                        # Keep existing content, but ensure ordering/title/duration are consistent.
                        updates = {}
                        if lesson.title != title:
                            updates["title"] = title
                        if lesson.order != order:
                            updates["order"] = order
                        expected_duration = 20 if difficulty == "Beginner" else 30 if difficulty == "Intermediate" else 40
                        if int(lesson.duration or 0) != expected_duration:
                            updates["duration"] = expected_duration
                        if updates:
                            for key, value in updates.items():
                                setattr(lesson, key, value)
                            lesson.save(update_fields=list(updates.keys()))
                    else:
                        created_lessons += 1

                    quiz_title = f"{title} Quiz ({difficulty})"
                    quiz, q_created = Quiz.objects.get_or_create(
                        lesson_id=lesson.id,
                        title=quiz_title,
                    )
                    if q_created:
                        created_quizzes += 1
                    # Ensure questions exist (reset if incomplete)
                    existing_q = Question.objects.filter(quiz_id=quiz.id).count()
                    if existing_q < 6:
                        Question.objects.filter(quiz_id=quiz.id).delete()
                        for spec in _quiz_questions_for(title):
                            Question.objects.create(
                                quiz_id=quiz.id,
                                text=spec["text"],
                                type="mcq",
                                options=spec["options"],
                                points=spec["points"],
                            )
                            created_questions += 1

                    challenge_title = f"{title} Challenge ({difficulty})"
                    _, ch_created = Challenge.objects.get_or_create(
                        lesson_id=lesson.id,
                        title=challenge_title,
                        defaults={
                            "description": f"Solve a small task related to: {title}.",
                            "initial_code": "class Example:\n    pass\n\nprint('Ready')\n",
                            "solution_code": None,
                            "test_cases": [{"input": "", "expected": "Ready"}],
                            "points": 10 if difficulty == "Beginner" else 20 if difficulty == "Intermediate" else 30,
                        },
                    )
                    if ch_created:
                        created_challenges += 1

            # Lesson profiles for ALL lessons (topic + prerequisites)
            topic_by_module_order = {
                1: "Python Basics",
                2: "Control Flow",
                3: "Loops",
                4: "Data Structures",
                5: "Functions",
                6: "OOP",
            }
            for lesson in Lesson.objects.all().only("id", "module_id", "difficulty", "order").iterator():
                module = Module.objects.filter(id=lesson.module_id).only("order").first()
                topic = topic_by_module_order.get(module.order if module else None) or "Python"
                prereq_ids = []
                if int(lesson.order or 0) > 1:
                    prev = Lesson.objects.filter(
                        module_id=lesson.module_id,
                        difficulty=lesson.difficulty,
                        order=int(lesson.order) - 1,
                    ).only("id").first()
                    if prev:
                        prereq_ids = [prev.id]
                LessonProfile.objects.update_or_create(
                    lesson_id=lesson.id,
                    defaults={
                        "topic": topic,
                        "difficulty": lesson.difficulty or "Beginner",
                        "prerequisites": prereq_ids,
                        "embedding_vector": [],
                    },
                )
                upserted_profiles += 1

        # Reuse existing seed commands where available
        try:
            call_command("seed_certificate_templates")
        except Exception:
            pass
        try:
            call_command("seed_sample_challenges")
        except Exception:
            pass
        try:
            # Ensure at least one 30-question placement diagnostic exists
            call_command("seed_structured_diagnostic_quiz")
        except Exception:
            pass

        self.stdout.write(self.style.SUCCESS(
            "Seed complete. "
            f"modules+{created_modules}, lessons+{created_lessons}, quizzes+{created_quizzes}, "
            f"questions+{created_questions}, challenges~{created_challenges}, profiles~{upserted_profiles} "
            f"at {timezone.now().isoformat(timespec='seconds')}"
        ))

