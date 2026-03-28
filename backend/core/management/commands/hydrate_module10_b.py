"""python manage.py hydrate_module10_b -- Module 10 Projects Lessons 6-10"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Lesson, Quiz, Question, Challenge

LESSONS = {
    # ── Lesson 6: Animal Kingdom Simulation ──────────────────────────────────
    "les-real-world-projects-6-beginner": {
        "title": "Capstone: Animal Inheritance Tree",
        "content": """# Capstone: Animal Inheritance Tree

## 🎯 Goal
Build a deep inheritance tree for an Animal Kingdom simulation.

## 📝 Structure
- `Animal`: Base class with `eat()` and `sleep()`.
- `Mammal`, `Bird`: Inherit from `Animal`.
- `Dog`, `Cat`: Inherit from `Mammal`.
- `Eagle`, `Penguin`: Inherit from `Bird`.

## 🏆 Key Takeaways
- Use inheritance to build complex, logical models of the real world.
""",
        "questions": [],
        "challenge": {
            "title": "Deep Inheritance",
            "description": "Define `Animal`, then `Dog(Animal)`. Does `Dog` have access to `Animal` methods? Print 'Yes' or 'No'.",
            "initial_code": "# code check\n",
            "solution_code": "print('Yes')\n",
            "test_cases": [{"input": "", "expected": "Yes"}],
        },
    },

    "les-real-world-projects-6-intermediate": {
        "title": "Capstone: Interactive Zoo",
        "content": """# Capstone: Interactive Zoo

## 🎯 Goal
Build a system that allows a user to "add animals" to a Zoo and "hear them speak".

## 📚 Concepts
- Polymorphism: `animal.speak()` works for any animal.
- Lists: To store the zoo population.

```python
zoo = [Dog(), Cat(), Eagle()]
for a in zoo:
    print(a.speak())
```
""",
        "questions": [],
        "challenge": {
            "title": "Zoo Speaker",
            "description": "Create two animal instances from your classes and print the result of their `speak()` methods in a list.",
            "initial_code": "# zoo logic\n",
            "solution_code": "class D: def speak(self): return 'W'\nclass C: def speak(self): return 'M'\nprint([D().speak(), C().speak()])\n",
            "test_cases": [{"input": "", "expected": "['W', 'M']"}],
        },
    },

    "les-real-world-projects-6-pro": {
        "title": "Capstone: Abstract Ecosystem",
        "content": """# Capstone: Abstract Ecosystem

## 🎯 Goal
Enforce that every animal in your Zoo MUST implement a `speak()` method using ABCs.

## 📝 Features
- `BaseAnimal(ABC)`
- `@abstractmethod` `speak()`
- Error handling for invalid animal types.
""",
        "questions": [],
        "challenge": {
            "title": "ABC Zoo",
            "description": "Define abstract `speak()` in `Animal`. If `Dog` inherits but doesn't implement it, what error occurs? Print the error name.",
            "initial_code": "# error name\n",
            "solution_code": "print('TypeError')\n",
            "test_cases": [{"input": "", "expected": "TypeError"}],
        },
    },

    # ── Lesson 7: Banking API ────────────────────────────────────────────────
    "les-real-world-projects-7-beginner": {
        "title": "Capstone: Banking System Core",
        "content": """# Capstone: Banking System Core

## 🎯 Goal
Build a safe, encapsulated Bank Account.

## 📝 Features
- Private `__balance`.
- `deposit()` and `withdraw()` methods.
- Validation: No negative deposits.
""",
        "questions": [],
        "challenge": {
            "title": "Safe Deposit",
            "description": "Implement `deposit(amount)`. Set balance to 100, deposit 50, print result.",
            "initial_code": "class Bank:\n    def __init__(self): self.bal = 0\n",
            "solution_code": "class Bank:\n    def __init__(self): self.bal = 100\n    def deposit(self, a): self.bal += a\nb = Bank()\nb.deposit(50)\nprint(b.bal)\n",
            "test_cases": [{"input": "", "expected": "150"}],
        },
    },

    "les-real-world-projects-7-intermediate": {
        "title": "Capstone: Transaction Auditing",
        "content": """# Capstone: Transaction Auditing

## 🎯 Goal
Add a history of all transactions to the Bank Account.

## 📚 Logic
Whenever `deposit` or `withdraw` is called, append the details to `self.history = []`.
""",
        "questions": [],
        "challenge": {
            "title": "Audit Log",
            "description": "Add 3 transactions to `history`. Print the length of the list.",
            "initial_code": "# audit logic\n",
            "solution_code": "h = []; h.append(1); h.append(2); h.append(3)\nprint(len(h))\n",
            "test_cases": [{"input": "", "expected": "3"}],
        },
    },

    "les-real-world-projects-7-pro": {
        "title": "Capstone: Multinational Bank (Currency)",
        "content": """# Capstone: Multinational Bank (Currency)

## 🎯 Goal
Handle multiple currencies (USD, EUR) using a conversion logic.

## 📝 Features
- `convert(amount, from, to)` utility method.
- Store balance in a base currency.
- Display in any requested currency.
""",
        "questions": [],
        "challenge": {
            "title": "FX Logic",
            "description": "If 1 USD = 0.9 EUR, write a function `to_eur(usd)` that returns the euro value. Print `to_eur(100)`.",
            "initial_code": "# math\n",
            "solution_code": "def to_eur(u): return u * 0.9\nprint(to_eur(100))\n",
            "test_cases": [{"input": "", "expected": "90.0"}],
        },
    },

    # ── Lesson 8: Performance Monitor ────────────────────────────────────────
    "les-real-world-projects-8-beginner": {
        "title": "Capstone: Function Timer",
        "content": """# Capstone: Function Timer

## 🎯 Goal
Write a decorator that times any function to find bottlenecks.

```python
import time

def time_it(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(f"Time: {time.time() - start}")
        return res
    return wrapper
```
""",
        "questions": [],
        "challenge": {
            "title": "Deco Build",
            "description": "Which Python module provides `time.time()`? Print its name.",
            "initial_code": "# module name\n",
            "solution_code": "print('time')\n",
            "test_cases": [{"input": "", "expected": "time"}],
        },
    },

    "les-real-world-projects-8-intermediate": {
        "title": "Capstone: Expensive Cache",
        "content": """# Capstone: Expensive Cache

## 🎯 Goal
Build a decorator that saves the results of expensive calculations so they don't have to be re-run!

## 📚 Concepts
- Closures: To store the cache dictionary.
- Decorators: To wrap the target function.
""",
        "questions": [],
        "challenge": {
            "title": "Cache Check",
            "description": "If a cache has 'key1', should you run the function or return the value? Print 'RUN' or 'VALUE'.",
            "initial_code": "# choice\n",
            "solution_code": "print('VALUE')\n",
            "test_cases": [{"input": "", "expected": "VALUE"}],
        },
    },

    "les-real-world-projects-8-pro": {
        "title": "Capstone: System Dashboard (psutil)",
        "content": """# Capstone: System Dashboard (psutil)

## 🎯 Goal
Scrape and display real-time CPU and RAM usage on your machine.

## 🛠️ The Tool
The `psutil` library.

```python
import psutil
print(psutil.cpu_percent())
print(psutil.virtual_memory().percent)
```
""",
        "questions": [],
        "challenge": {
            "title": "Stat Puller",
            "description": "What does CPU percent represent? Print 'Usage'.",
            "initial_code": "# answer\n",
            "solution_code": "print('Usage')\n",
            "test_cases": [{"input": "", "expected": "Usage"}],
        },
    },

    # ── Lesson 9: Dynamic Plugin Loader ──────────────────────────────────────
    "les-real-world-projects-9-beginner": {
        "title": "Capstone: Plugin Architecture",
        "content": """# Capstone: Plugin Architecture

## 🎯 Goal
Build a system where you can drop a `.py` file into a folder and it automatically adds a new feature.

## 📝 Logic
1. Scan `plugins/` folder.
2. Import each module.
3. Call the `run()` function inside.
""",
        "questions": [],
        "challenge": {
            "title": "List Plugins",
            "description": "Use `os.listdir('.')` to list files. Print the result.",
            "initial_code": "import os\n# list dir\n",
            "solution_code": "import os\nprint(os.listdir('.'))\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-real-world-projects-9-intermediate": {
        "title": "Capstone: Safe Dynamic Import",
        "content": """# Capstone: Safe Dynamic Import

## 🎯 Goal
Use `importlib` to load modules from strings.

```python
import importlib
module_name = "math"
m = importlib.import_module(module_name)
print(m.sqrt(16))
```
""",
        "questions": [],
        "challenge": {
            "title": "Lib Loader",
            "description": "What is the name of the built-in module used to import other modules by string name?",
            "initial_code": "# answer\n",
            "solution_code": "print('importlib')\n",
            "test_cases": [{"input": "", "expected": "importlib"}],
        },
    },

    "les-real-world-projects-9-pro": {
        "title": "Capstone: Full App Registry",
        "content": """# Capstone: Full App Registry

## 🎯 Goal
Build a registry where plugins register themselves automatically using a decorator.

```python
REGISTRY = {}

def register(name):
    def wrapper(cls):
        REGISTRY[name] = cls
        return cls
    return wrapper

@register("math")
class MathPlugin: pass
```
""",
        "questions": [],
        "challenge": {
            "title": "Reg Count",
            "description": "If `REGISTRY` has 5 entries, what is `len(REGISTRY)`? Print it.",
            "initial_code": "# count\n",
            "solution_code": "print(5)\n",
            "test_cases": [{"input": "", "expected": "5"}],
        },
    },

    # ── Lesson 10: Final Assessment ──────────────────────────────────────────
    "les-real-world-projects-10-beginner": {
        "title": "Capstone: The Python Final Boss",
        "content": """# Capstone: The Python Final Boss

## 🎯 Goal
Review everything from Module 1 to 10.

## 📝 The Challenge
Build a "Personal Knowledge Assistant" CLI.
- It can store notes (File IO).
- It can fetch weather (API/Requests).
- It has a user profile (OOP).
- It logs its own performance (Decorators).

Good luck!
""",
        "questions": [],
        "challenge": {
            "title": "Final Knowledge",
            "description": "Print 'I am ready' to complete the curriculum.",
            "initial_code": "# final print\n",
            "solution_code": "print('I am ready')\n",
            "test_cases": [{"input": "", "expected": "I am ready"}],
        },
    },

    "les-real-world-projects-10-intermediate": {
        "title": "Capstone: Deployment & Performance",
        "content": """# Capstone: Deployment & Performance

## 🎯 Goal
Package your CLI app for others to use.

## 📚 Concepts
- `setup.py` / `pyproject.toml`
- Virtual environments.
- Distributing on PyPI.
""",
        "questions": [],
        "challenge": {
            "title": "Env Magic",
            "description": "What command creates a virtual environment? Print 'venv'.",
            "initial_code": "# command\n",
            "solution_code": "print('venv')\n",
            "test_cases": [{"input": "", "expected": "venv"}],
        },
    },

    "les-real-world-projects-10-pro": {
        "title": "Capstone: The Future of Python",
        "content": """# Capstone: The Future of Python

## 🎯 Goal
Explore AI integration and high-performance Python.

## 📝 Topics
- Python in Machine Learning (PyTorch, TensorFlow).
- Python in AI (LangChain, OpenAI API).
- FastAPI and modern web development.

Congratulations! You have completed the High-Fidelity Python Curriculum.
""",
        "questions": [],
        "challenge": {
            "title": "Completion Cert",
            "description": "Print 'Master' to finish the Pro track.",
            "initial_code": "# finish\n",
            "solution_code": "print('Master')\n",
            "test_cases": [{"input": "", "expected": "Master"}],
        },
    },
}

class Command(BaseCommand):
    help = "Hydrate Module 10 (Projects) — Lessons 6-10"

    def handle(self, *args, **options):
        count = 0
        with transaction.atomic():
            for lesson_id, data in LESSONS.items():
                updated = Lesson.objects.filter(id=lesson_id).update(
                    title=data["title"], content=data["content"]
                )
                if not updated:
                    self.stdout.write(self.style.WARNING(f"  ⚠  Not found: {lesson_id}"))
                    continue
                
                # Add Quiz
                quiz, _ = Quiz.objects.get_or_create(
                    id=f"quiz-{lesson_id}",
                    defaults={"lesson_id": lesson_id, "title": f"Quiz: {data['title']}"}
                )
                Question.objects.filter(quiz_id=quiz.id).delete()
                for i, q in enumerate(data["questions"]):
                    Question.objects.create(
                        id=f"q-{lesson_id}-{i+1}",
                        quiz_id=quiz.id,
                        text=q["text"],
                        type="mcq",
                        options=q["options"],
                        points=5
                    )

                # Add Challenge
                ch = data["challenge"]
                Challenge.objects.filter(lesson_id=lesson_id).delete()
                Challenge.objects.create(
                    lesson_id=lesson_id,
                    title=ch["title"],
                    description=ch["description"],
                    initial_code=ch["initial_code"],
                    solution_code=ch["solution_code"],
                    test_cases=ch["test_cases"],
                    points=20
                )
                count += 1
                self.stdout.write(f"  ✅ {lesson_id}")
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Hydrated {count} lessons in Module 10 (6-10)"))
