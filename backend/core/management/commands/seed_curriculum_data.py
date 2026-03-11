from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Iterable

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify

from core.models import Module, Lesson, Quiz, Question, Challenge, CertificateTemplate
from lessons.models import LessonProfile
from gamification.models import Badge as GamificationBadge
from core.models import Badge as CoreBadge


@dataclass(frozen=True)
class LessonSpec:
    module_order: int
    lesson_order: int
    title: str
    topic: str
    difficulty: str = "Beginner"
    duration: int = 20  # minutes


MODULES = [
    (1, "Python Fundamentals", "Core syntax, variables, types, I/O, and basics to start writing Python confidently."),
    (2, "Control Flow", "Conditionals and boolean logic to make programs make decisions."),
    (3, "Loops", "Iteration patterns with for/while loops, range, and loop control."),
    (4, "Functions", "Reusable functions, parameters, return values, scope, and basic testing."),
    (5, "Data Structures", "Lists, tuples, sets, dictionaries, and common patterns."),
    (6, "Object Oriented Programming", "Classes, objects, methods, inheritance, and design thinking."),
]


def _lesson_markdown(spec: LessonSpec) -> str:
    # Store structured educational content in Lesson.content (markdown).
    # The UI already renders markdown in `LessonView`.
    example_code = {
        "variables": 'name = "Alice"\nage = 21\nprint(name, age)\n',
        "types": "x = 10\npi = 3.14\nflag = True\nprint(type(x), type(pi), type(flag))\n",
        "input_output": 'name = input("Name? ")\nprint("Hello", name)\n',
        "if_else": "x = 7\nif x % 2 == 0:\n    print('even')\nelse:\n    print('odd')\n",
        "loops_for": "for i in range(3):\n    print(i)\n",
        "loops_while": "n = 3\nwhile n > 0:\n    print(n)\n    n -= 1\n",
        "functions_def": "def add(a, b):\n    return a + b\n\nprint(add(2, 3))\n",
        "lists": "nums = [1, 2, 3]\nnums.append(4)\nprint(nums)\n",
        "dicts": "scores = {'A': 90, 'B': 80}\nprint(scores['A'])\n",
        "classes": "class Person:\n    def __init__(self, name):\n        self.name = name\n\np = Person('Alice')\nprint(p.name)\n",
    }.get(spec.topic, "print('Hello, Python!')\n")

    output_text = {
        "variables": "Alice 21",
        "loops_for": "0\n1\n2",
        "functions_def": "5",
        "lists": "[1, 2, 3, 4]",
        "dicts": "90",
        "classes": "Alice",
    }.get(spec.topic, "Hello, Python!")

    real_world = {
        1: "Store user profile data, settings, and configuration values.",
        2: "Validate user input and branch logic in applications.",
        3: "Process lists of records and repeat tasks efficiently.",
        4: "Organize code into reusable units and build clean APIs.",
        5: "Represent real data (tables, mappings) and transform collections.",
        6: "Model real-world entities and keep code maintainable as it grows.",
    }.get(spec.module_order, "Use this concept to write clearer, reusable programs.")

    takeaways = {
        "variables": [
            "Variables don’t need type declarations in Python.",
            "Names should be descriptive and follow snake_case.",
            "Values can be reassigned at runtime.",
        ],
        "if_else": [
            "Conditions evaluate to True/False.",
            "Use elif for multiple branches.",
            "Keep conditions readable with parentheses when needed.",
        ],
    }.get(spec.topic, ["Practice with a small example and confirm the output.", "Use this in a small real-world script."])

    return "\n\n".join(
        [
            f"# {spec.title}",
            f"**Topic**: `{spec.topic}`  \n**Difficulty**: `{spec.difficulty}`  \n**Estimated Duration**: {spec.duration} minutes",
            "## Concept Explanation",
            f"This lesson focuses on **{spec.title}** and how it fits into practical Python programming.",
            "## Syntax",
            "```python\n# See the example below\n```",
            "## Example Code",
            f"```python\n{example_code}```",
            "## Output",
            f"```\n{output_text}\n```",
            "## Real-world Use Case",
            real_world,
            "## Key Takeaways",
            "\n".join([f"- {t}" for t in takeaways]),
        ]
    )


def _question_bank(spec: LessonSpec) -> list[dict]:
    # 2 questions per lesson -> 120 total for 60 lessons.
    q1 = {
        "text": f"[{spec.topic}] What is the main purpose of {spec.title.lower()}?",
        "options": [
            {"text": "To solve a problem by applying a Python concept", "correct": True},
            {"text": "To configure a database server", "correct": False},
            {"text": "To install packages in Node.js", "correct": False},
            {"text": "To compile Python into C", "correct": False},
        ],
        "points": 2,
    }
    q2 = {
        "text": f"[{spec.topic}] Which option is a best practice related to this lesson?",
        "options": [
            {"text": "Keep code readable and test with small inputs", "correct": True},
            {"text": "Avoid using variables and functions", "correct": False},
            {"text": "Always use global state for simplicity", "correct": False},
            {"text": "Write everything in one long file", "correct": False},
        ],
        "points": 2,
    }
    return [q1, q2]


def _challenge_spec(spec: LessonSpec) -> dict:
    # Generate realistic beginner-level tasks by topic
    mapping = {
        "input_output": {
            "title": "Print Hello World",
            "description": "Write a program that prints Hello World",
            "starter": "\n".join([
                "def solve():",
                "    # print Hello World",
                "    print('Hello World')",
                "",
                "if __name__ == '__main__':",
                "    solve()",
                ""
            ]),
            "tests": [{"input": "", "expected": "Hello World"}],
        },
        "variables": {
            "title": "Input Name and Greet",
            "description": "Read a name and print 'Hello <name>'",
            "starter": "\n".join([
                "def solve():",
                "    name = input().strip()",
                "    print('Hello ' + name)",
                "",
                "if __name__ == '__main__':",
                "    solve()",
                ""
            ]),
            "tests": [{"input": "Alice", "expected": "Hello Alice"}, {"input": "Bob", "expected": "Hello Bob"}],
        },
        "if_else": {
            "title": "Even or Odd Checker",
            "description": "Read an integer and print 'Even' or 'Odd'",
            "starter": "\n".join([
                "def solve():",
                "    n = int(input().strip())",
                "    print('Even' if n % 2 == 0 else 'Odd')",
                "",
                "if __name__ == '__main__':",
                "    solve()",
                ""
            ]),
            "tests": [{"input": "2", "expected": "Even"}, {"input": "7", "expected": "Odd"}],
        },
        "loops_for": {
            "title": "Sum of N Numbers",
            "description": "Read N and then N integers; print their sum",
            "starter": "\n".join([
                "def solve():",
                "    n = int(input().strip())",
                "    total = 0",
                "    for _ in range(n):",
                "        total += int(input().strip())",
                "    print(total)",
                "",
                "if __name__ == '__main__':",
                "    solve()",
                ""
            ]),
            "tests": [{"input": "3\n1\n2\n3\n", "expected": "6"}, {"input": "4\n5\n5\n5\n5\n", "expected": "20"}],
        },
        "functions_def": {
            "title": "Factorial Function",
            "description": "Read n and print n! using a function",
            "starter": "\n".join([
                "def fact(n):",
                "    res = 1",
                "    for i in range(2, n+1):",
                "        res *= i",
                "    return res",
                "",
                "def solve():",
                "    n = int(input().strip())",
                "    print(fact(n))",
                "",
                "if __name__ == '__main__':",
                "    solve()",
                ""
            ]),
            "tests": [{"input": "4", "expected": "24"}, {"input": "0", "expected": "1"}],
        },
        "lists": {
            "title": "Reverse String",
            "description": "Read a string and print it reversed",
            "starter": "\n".join([
                "def solve():",
                "    s = input().strip()",
                "    print(s[::-1])",
                "",
                "if __name__ == '__main__':",
                "    solve()",
                ""
            ]),
            "tests": [{"input": "abc", "expected": "cba"}, {"input": "Python", "expected": "nohtyP"}],
        },
        "dicts": {
            "title": "Dictionary Lookup",
            "description": "Read key:value pairs count k, then k pairs; then read a key and print its value or 'Not found'",
            "starter": "\n".join([
                "def solve():",
                "    n = int(input().strip())",
                "    d = {}",
                "    for _ in range(n):",
                "        line = input().strip()",
                "        key, val = line.split(':', 1)",
                "        d[key.strip()] = val.strip()",
                "    q = input().strip()",
                "    print(d.get(q, 'Not found'))",
                "",
                "if __name__ == '__main__':",
                "    solve()",
                ""
            ]),
            "tests": [{"input": "2\nname: Alice\nage: 21\nname\n", "expected": "Alice"}, {"input": "1\nx: 10\ny\n", "expected": "Not found"}],
        },
        "classes": {
            "title": "Class with Constructor",
            "description": "Define a class Person with name, read a name, create Person, print name",
            "starter": "\n".join([
                "class Person:",
                "    def __init__(self, name):",
                "        self.name = name",
                "",
                "def solve():",
                "    n = input().strip()",
                "    p = Person(n)",
                "    print(p.name)",
                "",
                "if __name__ == '__main__':",
                "    solve()",
                ""
            ]),
            "tests": [{"input": "Alice", "expected": "Alice"}],
        },
    }
    entry = mapping.get(spec.topic) or {
        "title": f"{spec.title} Practice",
        "description": "Write a small program that prints a simple result.",
        "starter": "\n".join([
            "def solve():",
            "    print('OK')",
            "",
            "if __name__ == '__main__':",
            "    solve()",
            ""
        ]),
        "tests": [{"input": "", "expected": "OK"}],
    }
    return {
        "title": entry["title"],
        "description": entry["description"],
        "initial_code": entry["starter"],
        "solution_code": None,
        "test_cases": entry["tests"],
        "points": 20,
    }


def _build_specs() -> list[LessonSpec]:
    # 10 lessons per module -> 60 lessons total.
    module_topics: dict[int, list[tuple[str, str]]] = {
        1: [
            ("Python Setup & First Program", "input_output"),
            ("Variables", "variables"),
            ("Data Types", "types"),
            ("Operators", "operators"),
            ("Strings Basics", "strings"),
            ("Numbers & Math", "numbers"),
            ("Type Casting", "casting"),
            ("Comments & Style", "style"),
            ("Debugging Basics", "debugging"),
            ("Mini Project: Greeting App", "mini_project_1"),
        ],
        2: [
            ("Booleans & Comparisons", "booleans"),
            ("if / else", "if_else"),
            ("elif Chains", "elif"),
            ("Logical Operators", "logic_ops"),
            ("Nested Conditions", "nested_if"),
            ("Membership Operators", "membership"),
            ("Ternary Expressions", "ternary"),
            ("Input Validation", "validation"),
            ("Error Handling Intro", "exceptions_intro"),
            ("Mini Project: Eligibility Checker", "mini_project_2"),
        ],
        3: [
            ("for Loops", "loops_for"),
            ("while Loops", "loops_while"),
            ("range()", "range"),
            ("break / continue", "break_continue"),
            ("Loop Patterns", "loop_patterns"),
            ("Iterating Strings", "iterate_strings"),
            ("Nested Loops", "nested_loops"),
            ("Loop Efficiency", "loop_efficiency"),
            ("Practice: Counting & Summation", "counting"),
            ("Mini Project: Number Analyzer", "mini_project_3"),
        ],
        4: [
            ("Defining Functions", "functions_def"),
            ("Parameters & Arguments", "params_args"),
            ("Return Values", "return_values"),
            ("Scope (Local vs Global)", "scope"),
            ("Default Parameters", "defaults"),
            ("*args and **kwargs", "args_kwargs"),
            ("Recursion Intro", "recursion"),
            ("Docstrings", "docstrings"),
            ("Testing Basics", "testing"),
            ("Mini Project: Utility Functions", "mini_project_4"),
        ],
        5: [
            ("Lists", "lists"),
            ("List Methods", "list_methods"),
            ("Tuples", "tuples"),
            ("Sets", "sets"),
            ("Dictionaries", "dicts"),
            ("Dict Methods", "dict_methods"),
            ("Comprehensions", "comprehensions"),
            ("Sorting & Key Functions", "sorting"),
            ("Common DS Patterns", "ds_patterns"),
            ("Mini Project: Inventory Tracker", "mini_project_5"),
        ],
        6: [
            ("Classes and Objects", "classes"),
            ("Attributes and Methods", "methods"),
            ("Constructors (__init__)", "init"),
            ("Instance vs Class Variables", "class_vars"),
            ("Encapsulation", "encapsulation"),
            ("Inheritance", "inheritance"),
            ("Polymorphism", "polymorphism"),
            ("Composition", "composition"),
            ("Dunder Methods", "dunder"),
            ("Mini Project: Simple Bank Account", "mini_project_6"),
        ],
    }

    specs: list[LessonSpec] = []
    for module_order, lessons in module_topics.items():
        for idx, (title, topic) in enumerate(lessons, start=1):
            specs.append(LessonSpec(module_order=module_order, lesson_order=idx, title=title, topic=topic))
    return specs


def _chunk_iter(content: str, max_chars: int = 900) -> Iterable[str]:
    # Create a few LessonChunk records for RAG retrieval.
    # Keep it simple: chunk by paragraphs, then pack into chunks <= max_chars.
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    buf: list[str] = []
    size = 0
    for p in paragraphs:
        if size + len(p) + 2 > max_chars and buf:
            yield "\n\n".join(buf)
            buf = []
            size = 0
        buf.append(p)
        size += len(p) + 2
    if buf:
        yield "\n\n".join(buf)


class Command(BaseCommand):
    help = (
        "Seed a complete curriculum dataset into Django DB (modules/lessons/quizzes/questions/challenges/badges/certificates) "
        "and supporting LessonProfiles for prerequisites + adaptive topics. Safe to run multiple times."
    )

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Delete existing curriculum content before seeding.")

    def handle(self, *args, **options):
        reset = bool(options.get("reset"))
        lesson_specs = _build_specs()

        with transaction.atomic():
            if reset:
                Question.objects.all().delete()
                Quiz.objects.all().delete()
                Challenge.objects.all().delete()
                LessonProfile.objects.all().delete()
                Lesson.objects.all().delete()
                Module.objects.all().delete()

            # Modules
            module_by_order: dict[int, Module] = {}
            created_modules = 0
            for order, title, description in MODULES:
                module, created = Module.objects.get_or_create(
                    order=order,
                    defaults={"title": title, "description": description, "image_url": None},
                )
                if not created:
                    updates = {}
                    if module.title != title:
                        updates["title"] = title
                    if module.description != description:
                        updates["description"] = description
                    if updates:
                        for k, v in updates.items():
                            setattr(module, k, v)
                        module.save(update_fields=list(updates.keys()))
                else:
                    created_modules += 1
                module_by_order[order] = module

            # Certificates (templates) – ensure 5 exist (module completion certs)
            cert_templates = [
                ("cert-fundamentals", "Python Fundamentals Certificate", "Awarded after completing Python Fundamentals."),
                ("cert-control-flow", "Control Flow Certificate", "Awarded after completing Control Flow."),
                ("cert-loops", "Loops Certificate", "Awarded after completing Loops."),
                ("cert-functions", "Functions Certificate", "Awarded after completing Functions."),
                ("cert-data-structures", "Data Structures Certificate", "Awarded after completing Data Structures."),
            ]
            for code, title, desc in cert_templates:
                CertificateTemplate.objects.get_or_create(code=code, defaults={"title": title, "description": desc})

            # Badges – create 10 (in gamification + core for admin visibility)
            badges = [
                ("first-lesson", "First Lesson", "Complete your first lesson."),
                ("diagnostic-done", "Placement Completed", "Finish the placement diagnostic quiz."),
                ("streak-3", "3-Day Streak", "Maintain a 3-day learning streak."),
                ("streak-7", "7-Day Streak", "Maintain a 7-day learning streak."),
                ("quiz-starter", "Quiz Starter", "Complete 5 quizzes."),
                ("challenge-starter", "Challenge Starter", "Solve 3 coding challenges."),
                ("consistent-learner", "Consistent Learner", "Complete 10 lessons."),
                ("fast-learner", "Fast Learner", "Finish 5 lessons in a week."),
                ("oop-explorer", "OOP Explorer", "Complete the first OOP lesson."),
                ("python-pathfinder", "Python Pathfinder", "Complete one lesson in each module."),
            ]
            for code, title, desc in badges:
                GamificationBadge.objects.get_or_create(code=code, defaults={"title": title, "description": desc})
                CoreBadge.objects.get_or_create(name=title, defaults={"description": desc})

            # Lessons + Quizzes + Questions + LessonProfiles
            created_lessons = 0
            created_quizzes = 0
            created_questions = 0
            upserted_profiles = 0

            # Index existing for quick lookup
            for spec in lesson_specs:
                module = module_by_order[spec.module_order]
                slug = slugify(f"m{spec.module_order}-{spec.lesson_order}-{spec.title}")
                lesson, created = Lesson.objects.get_or_create(
                    module_id=module.id,
                    slug=slug,
                    difficulty=spec.difficulty,
                    defaults={
                        "title": spec.title,
                        "content": _lesson_markdown(spec),
                        "order": spec.lesson_order,
                        "duration": spec.duration,
                    },
                )
                if not created:
                    # Keep content editable in admin later; only ensure order/duration/title are stable.
                    updates = {}
                    if lesson.title != spec.title:
                        updates["title"] = spec.title
                    if int(lesson.order or 0) != spec.lesson_order:
                        updates["order"] = spec.lesson_order
                    if int(lesson.duration or 0) != spec.duration:
                        updates["duration"] = spec.duration
                    if updates:
                        for k, v in updates.items():
                            setattr(lesson, k, v)
                        lesson.save(update_fields=list(updates.keys()))
                else:
                    created_lessons += 1

                # Quiz (1 per lesson)
                quiz_title = f"{spec.title} Quiz"
                quiz, q_created = Quiz.objects.get_or_create(lesson_id=lesson.id, defaults={"title": quiz_title})
                if q_created:
                    created_quizzes += 1
                else:
                    if quiz.title != quiz_title:
                        quiz.title = quiz_title
                        quiz.save(update_fields=["title"])

                # Ensure exactly 2 questions per quiz
                desired = _question_bank(spec)
                existing_count = Question.objects.filter(quiz_id=quiz.id).count()
                if existing_count != len(desired):
                    Question.objects.filter(quiz_id=quiz.id).delete()
                    for q in desired:
                        Question.objects.create(
                            quiz_id=quiz.id,
                            text=q["text"],
                            type="mcq",
                            options=q["options"],
                            points=q["points"],
                        )
                        created_questions += 1

                # LessonProfile: topic + prereqs (previous lesson in module)
                prereq_ids = []
                if spec.lesson_order > 1:
                    prev_slug = slugify(f"m{spec.module_order}-{spec.lesson_order-1}-{lesson_specs[(spec.module_order-1)*10 + (spec.lesson_order-2)].title}")
                    prev = Lesson.objects.filter(module_id=module.id, slug=prev_slug, difficulty=spec.difficulty).only("id").first()
                    if prev:
                        prereq_ids = [prev.id]

                LessonProfile.objects.update_or_create(
                    lesson_id=lesson.id,
                    defaults={
                        "topic": spec.topic,
                        "difficulty": spec.difficulty,
                        "prerequisites": prereq_ids,
                        "embedding_vector": [],
                    },
                )
                upserted_profiles += 1

            # Challenges – ~30 challenges attached to the first 30 lessons
            created_challenges = 0
            first_30 = lesson_specs[:30]
            for spec in first_30:
                module = module_by_order[spec.module_order]
                slug = slugify(f"m{spec.module_order}-{spec.lesson_order}-{spec.title}")
                lesson = Lesson.objects.filter(module_id=module.id, slug=slug, difficulty=spec.difficulty).first()
                if not lesson:
                    continue
                ch = _challenge_spec(spec)
                _, ch_created = Challenge.objects.get_or_create(
                    lesson_id=lesson.id,
                    title=ch["title"],
                    defaults={
                        "description": ch["description"],
                        "initial_code": ch["initial_code"],
                        "solution_code": ch["solution_code"],
                        "test_cases": ch["test_cases"],
                        "points": ch["points"],
                    },
                )
                if ch_created:
                    created_challenges += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Curriculum seed complete. "
                f"modules+{created_modules}, lessons+{created_lessons}, quizzes+{created_quizzes}, "
                f"questions+{created_questions}, challenges+{created_challenges}, profiles~{upserted_profiles} "
                f"at {timezone.now().isoformat(timespec='seconds')}"
            )
        )
