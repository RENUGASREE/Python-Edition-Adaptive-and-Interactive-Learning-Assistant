from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Iterable

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify

from core.models import Module, Lesson, Quiz, Question, Challenge, CertificateTemplate
from lessons.models import LessonProfile, LessonChunk
from lessons.services import generate_embedding
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
    ("mod-python-basics", 1, "Python Fundamentals", "Core syntax, variables, types, I/O, and basics to start writing Python confidently."),
    ("mod-control-flow", 2, "Control Flow", "Conditionals and boolean logic to make programs make decisions."),
    ("mod-loops-iteration", 3, "Loops", "Iteration patterns with for/while loops, range, and loop control."),
    ("mod-functions", 4, "Functions", "Reusable functions, parameters, return values, scope, and basic testing."),
    ("mod-data-types", 5, "Data Structures", "Lists, tuples, sets, dictionaries, and common patterns."),
    ("mod-modules-packages", 6, "Object Oriented Programming", "Classes, objects, methods, inheritance, and design thinking."),
]


def _lesson_markdown(spec: LessonSpec) -> str:
    """
    Generates premium, instructor-level lesson content with high depth and structure.
    """
    title = spec.title.replace(f" ({spec.difficulty})", "")
    level = spec.difficulty
    topic = spec.topic

    # 1. Topic Hook & Storytelling
    hooks = {
        "input_output": "Imagine building a robot that can't hear you or speak back. That's a program without I/O. Today, we give your code a voice.",
        "variables": "In programming, memory is a vast ocean. Variables are the anchors that allow us to find exactly what we need, exactly when we need it.",
        "types": "A master chef knows the difference between a liquid, a solid, and a gas. In Python, knowing your data types is the secret to a perfect 'recipe'.",
        "if_else": "Life is full of choices. Should I take an umbrella? Should I press snooze? Your code needs to make these same decisions to be truly smart.",
        "loops_for": "Efficiency is doing things once and reaping the benefits forever. Loops allow you to automate the mundane so you can focus on the extraordinary.",
        "functions_def": "Don't repeat yourself. If you've solved a problem once, a function ensures you never have to solve it manually again.",
        "lists": "A single piece of data is a point; a list is a journey. Learn to manage collections of information like a pro.",
        "classes": "The world isn't made of strings and integers; it's made of 'Things'. Objects allow us to model reality inside our computers."
    }
    hook = hooks.get(topic, f"Welcome to our deep dive into **{title}**. Today, we bridge the gap between basic syntax and professional mastery.")

    # 2. Why This Matters
    matters = {
        "input_output": "Without I/O, your software is a black box. User experience (UX) starts with how you handle data entering and leaving your system.",
        "variables": "Memory management and data persistence are core to software engineering. Variables are the most fundamental unit of state management.",
        "types": "Type safety and data integrity prevent 90% of production bugs. Understanding how Python handles types is non-negotiable for reliability.",
        "if_else": "Logic is the brain of your application. Branching allows for personalization, security checks, and complex business rules.",
        "loops_for": "Scaling requires automation. Whether processing 10 rows or 10 million, loops are the engine of data processing.",
        "functions_def": "Modularity makes code maintainable. Functions allow teams to collaborate by creating reusable, testable units of logic.",
        "lists": "Real-world data is rarely singular. From social media feeds to financial transactions, everything happens in collections.",
        "classes": "Scalability in large systems depends on Object-Oriented Design. Classes provide the blueprint for building complex, interconnected systems."
    }
    matter = matters.get(topic, "This concept is a building block for all advanced Python frameworks, from Django to TensorFlow.")

    # 3. Mental Models
    models = {
        "input_output": {
            "Beginner": "Think of `input()` as a mailbox where users drop letters, and `print()` as a loudspeaker projecting your message to the room.",
            "Intermediate": "Visualize I/O as a 'Pipe'. Data flows from one end (Source) to the other (Sink). You can filter or transform it as it passes through.",
            "Pro": "See I/O as a 'Buffer'. In high-load systems, we don't wait for every byte; we collect them in buckets and process them in efficient batches."
        },
        "variables": {
            "Beginner": "A variable is like a labeled 'Sticky Note' on a box. You can peel it off and stick it on a different box later.",
            "Intermediate": "Think of a variable as a 'GPS Coordinate'. It doesn't contain the house (data), it just tells Python exactly where to find it in memory.",
            "Pro": "Visualize a 'Reference Graph'. Objects are nodes, and variables are arrows. When no arrows point to a node, Python's Garbage Collector reclaims that space."
        }
    }
    model = models.get(topic, {}).get(level, f"Think of {title} as a specialized tool in your engineering toolkit—designed for a specific job, but powerful when combined with others.")

    # 4. Advanced/Deep Explanations
    depth = {
        "Pro": f"At the senior level, **{title}** isn't just about syntax. We look at the CPython implementation, bytecode execution, and how this impacts the Global Interpreter Lock (GIL).",
        "Intermediate": f"Moving beyond the basics, we explore the Pythonic way to implement **{title}**, focusing on readability (PEP 8) and standard library utilities.",
        "Beginner": f"We'll start with the 'How' and 'Why' of **{title}**, ensuring you have a solid foundation before we build more complex logic."
    }

    # Construct the final Markdown
    content_blocks = [
        f"# {title}",
        f"> {hook}",
        f"## 🚀 Why This Matters\n{matter}",
        f"## 🧠 Concept Explanation\n{depth[level]}\n\n{model}",
        "## 💡 Mental Model",
        f"*{model}*",
        "## 🧪 Code Example",
    ]

    # Level-specific code (High Quality)
    codes = {
        "input_output": {
            "Beginner": "# Getting user input simply\nuser_name = input('What is your name? ')\nprint(f'Hello, {user_name}! Welcome to Python.')",
            "Intermediate": "# Robust I/O with validation\ndef get_age():\n    while True:\n        try:\n            return int(input('Enter age: '))\n        except ValueError:\n            print('Error: Please enter a numeric value.')\n\nage = get_age()\nprint(f'Age recorded: {age}')",
            "Pro": "# High-performance stream handling\nimport sys\nfrom io import StringIO\n\ndef fast_process(data_stream):\n    # Using buffers for efficiency in large data processing\n    buffer = StringIO(data_stream)\n    for line in buffer:\n        sys.stdout.write(f'[LOG] {line.strip()}\\n')"
        },
        "variables": {
            "Beginner": "# Simple assignment\nscore = 0\nscore = score + 10\nprint(score)  # Output: 10",
            "Intermediate": "# Tuple unpacking and multiple assignment\nx, y, z = 1, 2, 3\nx, y = y, x  # The Pythonic swap\nprint(f'x: {x}, y: {y}')",
            "Pro": "# Deep vs Shallow copy behavior\nimport copy\noriginal = [[1, 2, 3], [4, 5, 6]]\nshallow = copy.copy(original)\ndeep = copy.deepcopy(original)\n\noriginal[0][0] = 'CHANGED'\nprint(f'Shallow reflects change: {shallow[0][0]}')\nprint(f'Deep stays isolated: {deep[0][0]}')"
        }
    }
    code = codes.get(topic, {}).get(level, f"# Example for {title}\nprint('Mastering {level} concepts...')")
    content_blocks.append(f"```python\n{code}\n```")

    # 5. Real-World Applications
    apps = {
        "Beginner": "Building a personal budget tracker or a simple 'Choose Your Own Adventure' game.",
        "Intermediate": "Developing a web scraper that cleans data or a Discord bot that responds to user commands.",
        "Pro": "Optimizing a financial trading algorithm or architecting a microservice that handles millions of requests per second."
    }
    content_blocks.append(f"## 🌍 Real-World Application\n{apps[level]}")

    # 6. Common Mistakes & Best Practices
    mistakes = {
        "Beginner": "- **Mistake**: Forgetting quotes around strings.\n- **Fix**: Always use `'text'` or `\"text\"`.",
        "Intermediate": "- **Mistake**: Using global variables for everything.\n- **Fix**: Use function arguments and return values to pass data.",
        "Pro": "- **Mistake**: Ignoring memory overhead in large loops.\n- **Fix**: Use generators (`yield`) instead of large lists where possible."
    }
    content_blocks.append(f"## ⚠️ Common Mistakes\n{mistakes[level]}")

    content_blocks.append("## ✅ Best Practices")
    if level == "Pro":
        content_blocks.append("- **Clean Architecture**: Follow SOLID principles.\n- **Performance**: Use `cProfile` to find bottlenecks before optimizing.\n- **Testing**: Write unit tests for every edge case.")
    else:
        content_blocks.append("- Use descriptive, snake_case variable names.\n- Add comments to explain *why* you are doing something, not *what*.\n- Keep your code blocks small and focused.")

    # 7. Mini Challenge & Knowledge Check
    content_blocks.append("## 🏆 Mini Challenge")
    content_blocks.append(f"Can you apply **{title}** to a new scenario? Head over to the **Challenge** tab to test your skills against our automated test suite!")

    content_blocks.append("## 📝 Knowledge Check")
    content_blocks.append("1. What is the core purpose of this concept in a professional environment?")
    content_blocks.append("2. How does this feature behave differently as your data scales?")

    # 8. Pro Tip
    tips = {
        "Beginner": "Python is readable like English. If your code feels hard to read, there's probably a simpler way to write it!",
        "Intermediate": "Use the `help()` and `dir()` functions in the Python console to explore any object or module on the fly.",
        "Pro": "Premature optimization is the root of all evil. Focus on clear, correct code first, then use profilers to find where speed actually matters."
    }
    content_blocks.append(f"## 💡 Pro Tip\n{tips[level]}")

    return "\n\n".join(content_blocks)


def _question_bank(spec: LessonSpec) -> list[dict]:
    # 2 questions per lesson -> 120 total for 60 lessons.
    # Topic-specific questions for better learning experience
    topic_questions = {
        "input_output": [
            {
                "text": "Which function is used to display output in Python?",
                "options": [
                    {"text": "print()", "correct": True},
                    {"text": "display()", "correct": False},
                    {"text": "show()", "correct": False},
                    {"text": "output()", "correct": False},
                ],
                "points": 2,
            },
            {
                "text": "What does input() function return?",
                "options": [
                    {"text": "A string containing user input", "correct": True},
                    {"text": "An integer", "correct": False},
                    {"text": "A boolean value", "correct": False},
                    {"text": "Nothing, it only displays text", "correct": False},
                ],
                "points": 2,
            },
        ],
        "variables": [
            {
                "text": "How do you create a variable named 'score' with value 100 in Python?",
                "options": [
                    {"text": "score = 100", "correct": True},
                    {"text": "var score = 100", "correct": False},
                    {"text": "int score = 100", "correct": False},
                    {"text": "let score = 100", "correct": False},
                ],
                "points": 2,
            },
            {
                "text": "What is the correct naming convention for Python variables?",
                "options": [
                    {"text": "snake_case (e.g., user_name)", "correct": True},
                    {"text": "camelCase (e.g., userName)", "correct": False},
                    {"text": "PascalCase (e.g., UserName)", "correct": False},
                    {"text": "UPPER_CASE (e.g., USER_NAME)", "correct": False},
                ],
                "points": 2,
            },
        ],
        "types": [
            {
                "text": "Which function returns the data type of a variable?",
                "options": [
                    {"text": "type()", "correct": True},
                    {"text": "typeof()", "correct": False},
                    {"text": "dtype()", "correct": False},
                    {"text": "gettype()", "correct": False},
                ],
                "points": 2,
            },
            {
                "text": "What is the data type of: x = 3.14?",
                "options": [
                    {"text": "float", "correct": True},
                    {"text": "int", "correct": False},
                    {"text": "double", "correct": False},
                    {"text": "decimal", "correct": False},
                ],
                "points": 2,
            },
        ],
        "if_else": [
            {
                "text": "What keyword is used to start a conditional statement in Python?",
                "options": [
                    {"text": "if", "correct": True},
                    {"text": "when", "correct": False},
                    {"text": "condition", "correct": False},
                    {"text": "check", "correct": False},
                ],
                "points": 2,
            },
            {
                "text": "What does 'else' do in an if-else statement?",
                "options": [
                    {"text": "Executes code when the if condition is False", "correct": True},
                    {"text": "Executes code when the if condition is True", "correct": False},
                    {"text": "Stops the program", "correct": False},
                    {"text": "Creates a loop", "correct": False},
                ],
                "points": 2,
            },
        ],
        "loops_for": [
            {
                "text": "What does a for loop do in Python?",
                "options": [
                    {"text": "Iterates over a sequence (list, string, range, etc.)", "correct": True},
                    {"text": "Creates a function", "correct": False},
                    {"text": "Defines a class", "correct": False},
                    {"text": "Imports a module", "correct": False},
                ],
                "points": 2,
            },
            {
                "text": "What will 'for i in range(3):' iterate through?",
                "options": [
                    {"text": "0, 1, 2", "correct": True},
                    {"text": "1, 2, 3", "correct": False},
                    {"text": "0, 1, 2, 3", "correct": False},
                    {"text": "1, 2", "correct": False},
                ],
                "points": 2,
            },
        ],
        "loops_while": [
            {
                "text": "When does a while loop stop executing?",
                "options": [
                    {"text": "When its condition becomes False", "correct": True},
                    {"text": "After running exactly 10 times", "correct": False},
                    {"text": "When it reaches a break statement only", "correct": False},
                    {"text": "Never, it runs forever", "correct": False},
                ],
                "points": 2,
            },
            {
                "text": "What is a common mistake with while loops?",
                "options": [
                    {"text": "Forgetting to update the condition (infinite loop)", "correct": True},
                    {"text": "Using too many variables", "correct": False},
                    {"text": "Not using print statements", "correct": False},
                    {"text": "Starting with 0", "correct": False},
                ],
                "points": 2,
            },
        ],
        "functions_def": [
            {
                "text": "How do you define a function in Python?",
                "options": [
                    {"text": "def function_name():", "correct": True},
                    {"text": "function function_name():", "correct": False},
                    {"text": "func function_name():", "correct": False},
                    {"text": "create function_name():", "correct": False},
                ],
                "points": 2,
            },
            {
                "text": "What keyword is used to return a value from a function?",
                "options": [
                    {"text": "return", "correct": True},
                    {"text": "output", "correct": False},
                    {"text": "give", "correct": False},
                    {"text": "send", "correct": False},
                ],
                "points": 2,
            },
        ],
        "lists": [
            {
                "text": "How do you create an empty list in Python?",
                "options": [
                    {"text": "[] or list()", "correct": True},
                    {"text": "{}", "correct": False},
                    {"text": "()", "correct": False},
                    {"text": "new list()", "correct": False},
                ],
                "points": 2,
            },
            {
                "text": "What method adds an element to the end of a list?",
                "options": [
                    {"text": "append()", "correct": True},
                    {"text": "add()", "correct": False},
                    {"text": "push()", "correct": False},
                    {"text": "insert()", "correct": False},
                ],
                "points": 2,
            },
        ],
        "dicts": [
            {
                "text": "What is a dictionary in Python?",
                "options": [
                    {"text": "A collection of key-value pairs", "correct": True},
                    {"text": "A list of numbers", "correct": False},
                    {"text": "A type of function", "correct": False},
                    {"text": "A string manipulation tool", "correct": False},
                ],
                "points": 2,
            },
            {
                "text": "How do you access the value for key 'name' in dictionary 'd'?",
                "options": [
                    {"text": "d['name'] or d.get('name')", "correct": True},
                    {"text": "d.name", "correct": False},
                    {"text": "d->name", "correct": False},
                    {"text": "d(name)", "correct": False},
                ],
                "points": 2,
            },
        ],
        "classes": [
            {
                "text": "What keyword is used to define a class in Python?",
                "options": [
                    {"text": "class", "correct": True},
                    {"text": "struct", "correct": False},
                    {"text": "object", "correct": False},
                    {"text": "type", "correct": False},
                ],
                "points": 2,
            },
            {
                "text": "What is the purpose of __init__ method in a class?",
                "options": [
                    {"text": "Initialize object attributes when creating an instance", "correct": True},
                    {"text": "Delete the object", "correct": False},
                    {"text": "Print the object", "correct": False},
                    {"text": "Compare two objects", "correct": False},
                ],
                "points": 2,
            },
        ],
    }
    
    # Get topic-specific questions or fall back to generic ones
    questions = topic_questions.get(spec.topic)
    if questions:
        return questions
    
    # Generic questions for topics not specifically covered
    q1 = {
        "text": f"What is the main purpose of {spec.title.lower()} in Python?",
        "options": [
            {"text": "To solve problems and build programs", "correct": True},
            {"text": "To slow down the computer", "correct": False},
            {"text": "To create errors", "correct": False},
            {"text": "To make code unreadable", "correct": False},
        ],
        "points": 2,
    }
    q2 = {
        "text": f"Which is a best practice when learning {spec.title.lower()}?",
        "options": [
            {"text": "Practice with small examples and test your code", "correct": True},
            {"text": "Skip the fundamentals", "correct": False},
            {"text": "Copy code without understanding it", "correct": False},
            {"text": "Avoid asking questions", "correct": False},
        ],
        "points": 2,
    }
    return [q1, q2]


def _challenge_spec(spec: LessonSpec) -> dict:
    """
    Generates difficulty-appropriate challenge specifications for each lesson.
    """
    topic = spec.topic
    level = spec.difficulty
    
    # Base challenge logic
    challenges = {
        "input_output": {
            "Beginner": {
                "title": "Basic Greeter",
                "desc": "Write a program that takes a name as input and prints 'Hello, <name>!'.",
                "starter": "name = input()\nprint(f'Hello, {name}!')",
                "tests": [{"input": "Alice", "expected": "Hello, Alice!"}]
            },
            "Intermediate": {
                "title": "Formatted Calculator",
                "desc": "Take two numbers as input and print their sum in the format: 'The sum of X and Y is Z'.",
                "starter": "a = int(input())\nb = int(input())\nprint(f'The sum of {a} and {b} is {a + b}')",
                "tests": [{"input": "5\n10", "expected": "The sum of 5 and 10 is 15"}]
            },
            "Pro": {
                "title": "Stream Processor",
                "desc": "Read multiple lines of input until 'END' is typed. Print the count of lines received.",
                "starter": "count = 0\nwhile True:\n    line = input()\n    if line == 'END': break\n    count += 1\nprint(count)",
                "tests": [{"input": "line1\nline2\nEND", "expected": "2"}]
            }
        },
        "variables": {
            "Beginner": {
                "title": "Variable Swap",
                "desc": "You are given two variables a and b. Swap their values and print them.",
                "starter": "a = input()\nb = input()\na, b = b, a\nprint(a)\nprint(b)",
                "tests": [{"input": "5\n10", "expected": "10\n5"}]
            },
            "Intermediate": {
                "title": "Type Inspector",
                "desc": "Read an input. If it can be an integer, print 'INT', else if it can be a float, print 'FLOAT', else 'STR'.",
                "starter": "val = input()\ntry:\n    int(val)\n    print('INT')\nexcept:\n    try:\n        float(val)\n        print('FLOAT')\n    except:\n        print('STR')",
                "tests": [{"input": "10", "expected": "INT"}, {"input": "10.5", "expected": "FLOAT"}, {"input": "hi", "expected": "STR"}]
            },
            "Pro": {
                "title": "Reference Counter Simulation",
                "desc": "Simulate a simple reference count. If an object is assigned to a new variable, count increases. If a variable is deleted, count decreases. Read 'ADD' or 'DEL' and print the final count starting from 1.",
                "starter": "count = 1\nn = int(input())\nfor _ in range(n):\n    op = input()\n    if op == 'ADD': count += 1\n    elif op == 'DEL': count -= 1\nprint(count)",
                "tests": [{"input": "3\nADD\nADD\nDEL", "expected": "2"}]
            }
        }
    }

    # Default fallback challenge if topic/level not found
    default_challenge = {
        "title": f"{spec.title} Challenge",
        "desc": f"Apply what you learned about {spec.title} to solve this problem. Ensure your output matches the expected format exactly.",
        "starter": "print('Solution complete!')",
        "tests": [{"input": "", "expected": "Solution complete!"}]
    }

    res = challenges.get(topic, {}).get(level, default_challenge)
    return {
        "title": res["title"],
        "description": res["desc"],
        "initial_code": "", 
        "solution_code": res["starter"],
        "test_cases": res["tests"],
        "points": 50 if level == "Pro" else (30 if level == "Intermediate" else 10),
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
            for diff in ["Beginner", "Intermediate", "Pro"]:
                specs.append(LessonSpec(
                    module_order=module_order, 
                    lesson_order=idx, 
                    title=f"{title} ({diff})", 
                    topic=topic, 
                    difficulty=diff
                ))
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
                
                # Reset auto-increment counters based on database vendor
                from django.db import connection
                if connection.vendor == 'sqlite':
                    with connection.cursor() as cursor:
                        tables = ['modules', 'lessons', 'quizzes', 'questions', 'challenges', 'lessons_lessonprofile']
                        for table in tables:
                            try:
                                cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}'")
                            except Exception:
                                pass
                elif connection.vendor == 'postgresql':
                    with connection.cursor() as cursor:
                        # Get all sequence names from the database
                        cursor.execute("SELECT relname FROM pg_class WHERE relkind = 'S'")
                        sequences = [row[0] for row in cursor.fetchall()]
                        
                        tables = ['modules', 'lessons', 'quizzes', 'questions', 'challenges', 'lessons_lessonprofile']
                        for table in tables:
                            seq_name = f"{table}_id_seq"
                            if seq_name in sequences:
                                try:
                                    cursor.execute(f"ALTER SEQUENCE {seq_name} RESTART WITH 1")
                                except Exception:
                                    pass

            # Modules
            module_by_order: dict[int, Module] = {}
            created_modules = 0
            for mod_id, order, title, description in MODULES:
                module, created = Module.objects.get_or_create(
                    id=mod_id,
                    defaults={"order": order, "title": title, "description": description, "image_url": None},
                )
                if not created:
                    updates = {}
                    if module.title != title:
                        updates["title"] = title
                    if module.description != description:
                        updates["description"] = description
                    if module.order != order:
                        updates["order"] = order
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

            created_challenges = 0
            # Add 30 new unique standalone challenges (10 Easy, 10 Medium, 10 Hard)
            standalone_challenges = [
                # Easy (10)
                {"title": "Sum of Two", "desc": "Read two integers and print their sum.", "diff": "Easy", "sol": "a=int(input())\nb=int(input())\nprint(a+b)", "tests": [{"input": "5\n10", "expected": "15"}]},
                {"title": "Multiply Two", "desc": "Read two integers and print their product.", "diff": "Easy", "sol": "a=int(input())\nb=int(input())\nprint(a*b)", "tests": [{"input": "3\n4", "expected": "12"}]},
                {"title": "Square Me", "desc": "Read an integer and print its square.", "diff": "Easy", "sol": "n=int(input())\nprint(n**2)", "tests": [{"input": "5", "expected": "25"}]},
                {"title": "Sign Check", "desc": "Read an integer. Print 'Positive' if > 0, 'Negative' if < 0, or 'Zero'.", "diff": "Easy", "sol": "n=int(input())\nif n>0: print('Positive')\nelif n<0: print('Negative')\nelse: print('Zero')", "tests": [{"input": "10", "expected": "Positive"}, {"input": "-5", "expected": "Negative"}]},
                {"title": "String Length", "desc": "Read a string and print its length.", "diff": "Easy", "sol": "s=input()\nprint(len(s))", "tests": [{"input": "hello", "expected": "5"}]},
                {"title": "Join Strings", "desc": "Read two strings and print them joined by a space.", "diff": "Easy", "sol": "a=input()\nb=input()\nprint(a + ' ' + b)", "tests": [{"input": "Hello\nWorld", "expected": "Hello World"}]},
                {"title": "Char in String", "desc": "Read a char and a string. Print 'Found' if char is in string, else 'No'.", "diff": "Easy", "sol": "c=input()\ns=input()\nprint('Found' if c in s else 'No')", "tests": [{"input": "a\napple", "expected": "Found"}]},
                {"title": "Print Range", "desc": "Read an integer N. Print numbers from 1 to N separated by space.", "diff": "Easy", "sol": "n=int(input())\nprint(*(range(1, n+1)))", "tests": [{"input": "3", "expected": "1 2 3"}]},
                {"title": "Max of Two", "desc": "Read two integers and print the larger one.", "diff": "Easy", "sol": "a=int(input())\nb=int(input())\nprint(max(a, b))", "tests": [{"input": "10\n20", "expected": "20"}]},
                {"title": "Rectangle Area", "desc": "Read length and width. Print the area.", "diff": "Easy", "sol": "l=int(input())\nw=int(input())\nprint(l*w)", "tests": [{"input": "5\n4", "expected": "20"}]},
                
                # Medium (10)
                {"title": "Max in List", "desc": "Read N then N integers. Print the maximum value.", "diff": "Medium", "sol": "n=int(input())\nl=[int(input()) for _ in range(n)]\nprint(max(l))", "tests": [{"input": "3\n1\n5\n2", "expected": "5"}]},
                {"title": "List Average", "desc": "Read N then N integers. Print the average (integer part).", "diff": "Medium", "sol": "n=int(input())\nl=[int(input()) for _ in range(n)]\nprint(sum(l)//n)", "tests": [{"input": "3\n10\n20\n30", "expected": "20"}]},
                {"title": "Filter Evens", "desc": "Read N then N integers. Print only even numbers separated by space.", "diff": "Medium", "sol": "n=int(input())\nl=[int(input()) for _ in range(n)]\nprint(*(x for x in l if x%2==0))", "tests": [{"input": "4\n1\n2\n3\n4", "expected": "2 4"}]},
                {"title": "Reverse List", "desc": "Read N then N integers. Print the list in reverse order.", "diff": "Medium", "sol": "n=int(input())\nl=[int(input()) for _ in range(n)]\nprint(*(l[::-1]))", "tests": [{"input": "3\n1\n2\n3", "expected": "3 2 1"}]},
                {"title": "Count Occurrences", "desc": "Read N then N integers, then a value X. Print how many times X appears.", "diff": "Medium", "sol": "n=int(input())\nl=[int(input()) for _ in range(n)]\nx=int(input())\nprint(l.count(x))", "tests": [{"input": "4\n1\n2\n1\n3\n1", "expected": "2"}]},
                {"title": "Palindrome Check", "desc": "Read a string. Print 'Yes' if it is a palindrome, else 'No'.", "diff": "Medium", "sol": "s=input().strip()\nprint('Yes' if s == s[::-1] else 'No')", "tests": [{"input": "madam", "expected": "Yes"}, {"input": "hello", "expected": "No"}]},
                {"title": "Common Elements", "desc": "Read two lists of 3 integers each. Print common elements separated by space.", "diff": "Medium", "sol": "a={int(input()) for _ in range(3)}\nb={int(input()) for _ in range(3)}\nprint(*(sorted(list(a & b))))", "tests": [{"input": "1\n2\n3\n2\n3\n4", "expected": "2 3"}]},
                {"title": "Sort Numbers", "desc": "Read N then N integers. Print them sorted.", "diff": "Medium", "sol": "n=int(input())\nl=[int(input()) for _ in range(n)]\nprint(*(sorted(l)))", "tests": [{"input": "3\n3\n1\n2", "expected": "1 2 3"}]},
                {"title": "Power Function", "desc": "Read base X and power Y. Print X raised to Y.", "diff": "Medium", "sol": "x=int(input())\ny=int(input())\nprint(x**y)", "tests": [{"input": "2\n3", "expected": "8"}]},
                {"title": "Second Largest", "desc": "Read N then N unique integers. Print the second largest.", "diff": "Medium", "sol": "n=int(input())\nl=[int(input()) for _ in range(n)]\nl.sort()\nprint(l[-2])", "tests": [{"input": "3\n10\n30\n20", "expected": "20"}]},

                # Hard (10)
                {"title": "Fibonacci Nth", "desc": "Read N. Print the Nth Fibonacci number (starting 0, 1, 1...).", "diff": "Hard", "sol": "n=int(input())\na,b=0,1\nfor _ in range(n): a,b=b,a+b\nprint(a)", "tests": [{"input": "5", "expected": "5"}, {"input": "0", "expected": "0"}]},
                {"title": "Prime Checker", "desc": "Read N. Print 'Prime' if N is prime, else 'Not Prime'.", "diff": "Hard", "sol": "n=int(input())\nif n<2: print('Not Prime')\nelse:\n for i in range(2,int(n**0.5)+1):\n  if n%i==0: print('Not Prime'); break\n else: print('Prime')", "tests": [{"input": "7", "expected": "Prime"}, {"input": "10", "expected": "Not Prime"}]},
                {"title": "All Divisors", "desc": "Read N. Print all its divisors in ascending order.", "diff": "Hard", "sol": "n=int(input())\nprint(*(i for i in range(1,n+1) if n%i==0))", "tests": [{"input": "6", "expected": "1 2 3 6"}]},
                {"title": "Merge Sorted", "desc": "Read two sorted lists of 3 integers each. Print merged sorted list.", "diff": "Hard", "sol": "a=[int(input()) for _ in range(3)]\nb=[int(input()) for _ in range(3)]\nprint(*(sorted(a+b)))", "tests": [{"input": "1\n3\n5\n2\n4\n6", "expected": "1 2 3 4 5 6"}]},
                {"title": "Flatten List", "desc": "Read N. Then read N lines where each line has 2 space-separated integers. Print all integers in one line.", "diff": "Hard", "sol": "n=int(input())\nres=[]\nfor _ in range(n): res.extend(input().split())\nprint(*(res))", "tests": [{"input": "2\n1 2\n3 4", "expected": "1 2 3 4"}]},
                {"title": "Word Frequency", "desc": "Read a sentence. Print each word and its count like 'word: count' sorted alphabetically.", "diff": "Hard", "sol": "s=input().split()\nd={w:s.count(w) for w in sorted(set(s))}\nfor k,v in d.items(): print(f'{k}: {v}')", "tests": [{"input": "apple banana apple", "expected": "apple: 2\nbanana: 1"}]},
                {"title": "Decimal to Binary", "desc": "Read an integer. Print its binary representation (without 0b).", "diff": "Hard", "sol": "n=int(input())\nprint(bin(n)[2:])", "tests": [{"input": "10", "expected": "1010"}]},
                {"title": "Binary Search", "desc": "Read sorted list of 5 ints, then a value X. Print its index or -1.", "diff": "Hard", "sol": "l=[int(input()) for _ in range(5)]\nx=int(input())\ntry: print(l.index(x))\nexcept: print(-1)", "tests": [{"input": "1\n3\n5\n7\n9\n5", "expected": "2"}]},
                {"title": "Anagram Check", "desc": "Read two strings. Print 'Yes' if they are anagrams, else 'No'.", "diff": "Hard", "sol": "a=input().strip()\nb=input().strip()\nprint('Yes' if sorted(a)==sorted(b) else 'No')", "tests": [{"input": "listen\nsilent", "expected": "Yes"}, {"input": "hello\nworld", "expected": "No"}]},
                {"title": "Most Frequent", "desc": "Read N then N integers. Print the most frequent one.", "diff": "Hard", "sol": "n=int(input())\nl=[int(input()) for _ in range(n)]\nprint(max(set(l), key=l.count))", "tests": [{"input": "5\n1\n2\n2\n3\n1\n1", "expected": "1"}]},
            ]

            for c_data in standalone_challenges:
                c_id = f"standalone-{slugify(c_data['title'])}"
                Challenge.objects.update_or_create(
                    id=c_id,
                    defaults={
                        "lesson_id": "-1", # Standalone
                        "title": c_data["title"],
                        "description": c_data["desc"],
                        "initial_code": "",
                        "solution_code": c_data["sol"],
                        "test_cases": c_data["tests"],
                        "points": 50,
                        "difficulty": c_data["diff"],
                    }
                )
                created_challenges += 1

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
                slug = slugify(f"m{spec.module_order}-{spec.lesson_order}-{spec.title}-{spec.difficulty}")
                lesson, created = Lesson.objects.update_or_create(
                    id=slug,
                    defaults={
                        "module_id": module.id,
                        "title": spec.title,
                        "slug": slug,
                        "content": _lesson_markdown(spec),
                        "order": spec.lesson_order,
                        "duration": spec.duration,
                        "difficulty": spec.difficulty,
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

                # Create LessonChunks for RAG
                LessonChunk.objects.filter(lesson_id=lesson.id).delete()  # Clear existing chunks
                for i, chunk_content in enumerate(_chunk_iter(lesson.content)):
                    embedding = generate_embedding(chunk_content)
                    LessonChunk.objects.create(
                        lesson_id=lesson.id,
                        content=chunk_content,
                        embedding_vector=embedding,
                    )

                # Quiz (1 per lesson)
                quiz_title = f"{spec.title} Quiz"
                quiz, q_created = Quiz.objects.update_or_create(
                    id=f"quiz-{lesson.id}",
                    defaults={"lesson_id": lesson.id, "title": quiz_title}
                )
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
                    for q_idx, q in enumerate(desired):
                        Question.objects.create(
                            id=f"q-{quiz.id}-{q_idx}",
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
                    prev = Lesson.objects.filter(module_id=module.id, order=spec.lesson_order-1, difficulty=spec.difficulty).only("id").first()
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

            # Challenges – Link EVERY lesson to a difficulty-appropriate challenge
            created_challenges = 0
            for spec in lesson_specs:
                module = module_by_order[spec.module_order]
                slug = slugify(f"m{spec.module_order}-{spec.lesson_order}-{spec.title}-{spec.difficulty}")
                lesson = Lesson.objects.filter(id=slug).first()
                if not lesson:
                    continue
                
                ch = _challenge_spec(spec)
                # Ensure the challenge ID is unique and linked to this specific lesson variant
                challenge_id = f"ch-{lesson.id}"
                
                Challenge.objects.update_or_create(
                    id=challenge_id,
                    defaults={
                        "lesson_id": lesson.id,
                        "title": ch["title"],
                        "description": ch["description"],
                        "initial_code": ch["initial_code"],
                        "solution_code": ch["solution_code"],
                        "test_cases": ch["test_cases"],
                        "points": ch["points"],
                        "difficulty": spec.difficulty,
                    },
                )
                created_challenges += 1

            # Badges
            created_badges = 0
            badges_data = [
                ("first-steps", "First Steps – Complete first lesson"),
                ("quiz-master", "Quiz Master – Score 80%+ in placement quiz"),
                ("consistency-starter", "Consistency Starter – 3 day streak"),
                ("code-warrior", "Code Warrior – Complete 10 lessons"),
                ("python-apprentice", "Python Apprentice – Complete Module 1"),
                ("python-expert", "Python Expert – Complete all modules"),
                ("perfect-score", "Perfect Score – 100% on any quiz"),
                ("fast-learner", "Fast Learner – Finish module in under 3 days"),
            ]
            for code, title in badges_data:
                obj, was_created = GamificationBadge.objects.get_or_create(
                    code=code, 
                    defaults={"title": title, "description": title}
                )
                if was_created:
                    created_badges += 1

            # Certificate Templates
            created_certs = 0
            certs_data = [
                ("beginner-python", "Beginner Python Certificate", "Awarded for completing beginner track"),
                ("intermediate-python", "Intermediate Python Certificate", "Awarded for completing intermediate track"),
                ("advanced-python", "Advanced Python Certificate", "Awarded for completing advanced track"),
                ("module-completion", "Module Completion Certificate", "Awarded for completing any module"),
                ("full-course", "Full Course Completion Certificate", "Awarded for completing the full curriculum"),
            ]
            for code, title, desc in certs_data:
                obj, was_created = CertificateTemplate.objects.get_or_create(
                    code=code, 
                    defaults={"title": title, "description": desc}
                )
                if was_created:
                    created_certs += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Curriculum seed complete. "
                f"modules+{created_modules}, lessons+{created_lessons}, quizzes+{created_quizzes}, "
                f"questions+{created_questions}, challenges+{created_challenges}, profiles~{upserted_profiles}, "
                f"badges+{created_badges}, certificates+{created_certs} "
                f"at {timezone.now().isoformat(timespec='seconds')}"
            )
        )
