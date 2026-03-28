"""python manage.py hydrate_module9_b -- Module 9 Advanced Python Lessons 6-10"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Lesson, Quiz, Question, Challenge

LESSONS = {
    # ── Lesson 6: Context Managers ───────────────────────────────────────────
    "les-advanced-python-6-beginner": {
        "title": "The 'with' Statement",
        "content": """# The 'with' Statement

## 🎯 Learning Objectives
- Use context managers for automatic resource management
- Understand the "Enter" and "Exit" lifecycle
- Prevent resource leaks (files, database connections)

## 📚 Concept Overview
The `with` statement ensures that an object is "cleaned up" even if an error occurs.

```python
with open("file.txt", "w") as f:
    f.write("Hello")
# f.close() is called automatically here!
```

## 🏆 Key Takeaways
- Use `with` whenever you are dealing with external resources.
- It is significantly safer than manual `try...finally` blocks.
""",
        "questions": [
            {"text": "Which statement is used to invoke a context manager?", "options": [
                {"text": "with", "correct": True}, {"text": "using", "correct": False},
                {"text": "from", "correct": False}, {"text": "open", "correct": False}]},
            {"text": "What is the primary benefit of context managers?", "options": [
                {"text": "Guaranteed cleanup of resources", "correct": True},
                {"text": "Making code run faster", "correct": False},
                {"text": "Hiding private data", "correct": False},
                {"text": "Automatically importing modules", "correct": False}]},
        ],
        "challenge": {
            "title": "Safe Writer",
            "description": "Write a line of code that opens 'test.txt' for writing using the `with` statement and a file object named `f`.",
            "initial_code": "# write the with line\n",
            "solution_code": "with open('test.txt', 'w') as f:\n    pass\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-advanced-python-6-intermediate": {
        "title": "Custom Context Managers",
        "content": """# Custom Context Managers

## 🎯 Learning Objectives
- Implement the `__enter__` and `__exit__` methods
- Create classes that support the `with` statement
- Handle exceptions within the `__exit__` method

## 📚 Concept Overview
```python
class MyTimer:
    def __enter__(self):
        print("Starting timer...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Stopping timer...")

with MyTimer():
    print("Running work...")
```

## 🏆 Key Takeaways
- `__enter__` sets up the resource.
- `__exit__` cleans it up.
""",
        "questions": [
            {"text": "Which method is called at the END of a `with` block?", "options": [
                {"text": "__exit__", "correct": True}, {"text": "__enter__", "correct": False},
                {"text": "__del__", "correct": False}, {"text": "__stop__", "correct": False}]},
        ],
        "challenge": {
            "title": "Lifecycle Tracker",
            "description": "Implement a class `Trace` with `__enter__` and `__exit__`. Print 'IN' and 'OUT' respectively. Use it in a `with` block.",
            "initial_code": "class Trace:\n    # implement enter and exit\n    pass\n",
            "solution_code": "class Trace:\n    def __enter__(self): print('IN'); return self\n    def __exit__(self, a, b, c): print('OUT')\nwith Trace(): pass\n",
            "test_cases": [{"input": "", "expected": "IN\nOUT"}],
        },
    },

    "les-advanced-python-6-pro": {
        "title": "@contextmanager Decorator",
        "content": """# @contextmanager Decorator

## 🎯 Learning Objectives
- Use `contextlib.contextmanager` to create managers using generator functions
- Compare class-based vs function-based managers
- Simplify resource setup logic

## 📚 Concept Overview
Instead of a whole class, you can use a single function with `yield`.

```python
from contextlib import contextmanager

@contextmanager
def file_manager(name, mode):
    f = open(name, mode)
    try:
        yield f # The 'with' block runs here
    finally:
        f.close()
```

## 🏆 Key Takeaways
- Use the decorator for simple, lightweight context managers.
- Always use `try...finally` around the `yield` to ensure cleanup!
""",
        "questions": [
            {"text": "Which module provides the @contextmanager decorator?", "options": [
                {"text": "contextlib", "correct": True}, {"text": "sys", "correct": False},
                {"text": "math", "correct": False}, {"text": "os", "correct": False}]},
        ],
        "challenge": {
            "title": "Decorator Magic",
            "description": "Create a manager `temp_print()` that prints 'START', yields, then prints 'END'.",
            "initial_code": "from contextlib import contextmanager\n# def manager\n",
            "solution_code": "from contextlib import contextmanager\n@contextmanager\ndef temp_print():\n    print('START')\n    yield\n    print('END')\nwith temp_print(): pass\n",
            "test_cases": [{"input": "", "expected": "START\nEND"}],
        },
    },

    # ── Lesson 7: Map, Filter, Reduce ────────────────────────────────────────
    "les-advanced-python-7-beginner": {
        "title": "Map & Filter",
        "content": """# Map & Filter

## 🎯 Learning Objectives
- Transform lists using `map()`
- Pick items using `filter()`
- Understand the utility of Lambdas in functional programming

## 📚 Concept Overview
- **Map**: Apply a function to every item.
- **Filter**: Keep only items that return True.

```python
nums = [1, 2, 3, 4]
# Map: multiply by 2
res_map = list(map(lambda x: x * 2, nums))

# Filter: keep > 2
res_filter = list(filter(lambda x: x > 2, nums))
```

## 🏆 Key Takeaways
- These are often more "Functional" than comprehensions but can sometimes be harder to read.
- They return **Iterators**, so you must wrap them in `list()` to see the values.
""",
        "questions": [
            {"text": "Which function is used to apply a transformation to every item in an iterable?", "options": [
                {"text": "map", "correct": True}, {"text": "filter", "correct": False},
                {"text": "reduce", "correct": False}, {"text": "apply", "correct": False}]},
            {"text": "Which function is used to include only items that meet certain criteria?", "options": [
                {"text": "filter", "correct": True}, {"text": "map", "correct": False},
                {"text": "selector", "correct": False}, {"text": "choice", "correct": False}]},
        ],
        "challenge": {
            "title": "Square Mapper",
            "description": "Use `map` and a `lambda` to square all numbers in `[1, 2, 3]`. Print the result as a list.",
            "initial_code": "nums = [1, 2, 3]\n# use map\n",
            "solution_code": "nums = [1, 2, 3]\nprint(list(map(lambda x: x*x, nums)))\n",
            "test_cases": [{"input": "", "expected": "[1, 4, 9]"}],
        },
    },

    "les-advanced-python-7-intermediate": {
        "title": "The functools.reduce function",
        "content": """# The functools.reduce function

## 🎯 Learning Objectives
- "Reduce" a collection to a single value
- Understand cumulative operations
- Use initializers in reduction

## 📚 Concept Overview
`reduce` works by applying a function of two arguments cumulatively to the items of a sequence.

```python
from functools import reduce

nums = [1, 2, 3, 4]
sum_all = reduce(lambda x, y: x + y, nums) # ((1+2)+3)+4 = 10
```

## 🏆 Key Takeaways
- `reduce` moved to the `functools` module in Python 3 because a simple `sum()` or `for` loop is usually clearer.
""",
        "questions": [
            {"text": "Which module contains the `reduce` function?", "options": [
                {"text": "functools", "correct": True}, {"text": "math", "correct": False},
                {"text": "sys", "correct": False}, {"text": "collections", "correct": False}]},
        ],
        "challenge": {
            "title": "Factorial Reduction",
            "description": "Use `reduce` to calculate the product of `[1, 2, 3, 4]`. Print the result.",
            "initial_code": "from functools import reduce\nnums = [1, 2, 3, 4]\n# reduce to product\n",
            "solution_code": "from functools import reduce\nnums = [1, 2, 3, 4]\nprint(reduce(lambda x, y: x * y, nums))\n",
            "test_cases": [{"input": "", "expected": "24"}],
        },
    },

    "les-advanced-python-7-pro": {
        "title": "Currying & Partial Functions",
        "content": """# Currying & Partial Functions

## 🎯 Learning Objectives
- Fix some arguments of a function using `functools.partial`
- Understand the benefits of pre-filling arguments
- Simplify API calls

## 📚 Concept Overview
```python
from functools import partial

def multiply(x, y): return x * y

# Create a specialized function 'double'
double = partial(multiply, 2)
print(double(10)) # 20
```

## ️🏆 Key Takeaways
- `partial` allows you to create simpler versions of complex functions.
""",
        "questions": [
            {"text": "What is the name of the function used to pre-fill certain arguments of another function?", "options": [
                {"text": "partial", "correct": True}, {"text": "fixed", "correct": False},
                {"text": "preset", "correct": False}, {"text": "prefill", "correct": False}]},
        ],
        "challenge": {
            "title": "Octal Parser",
            "description": "Use `partial(int, base=8)` to create an `oct_to_int` function. Use it to parse the string '10' and print results.",
            "initial_code": "from functools import partial\n# use partial\n",
            "solution_code": "from functools import partial\noct_to_int = partial(int, base=8)\nprint(oct_to_int('10'))\n",
            "test_cases": [{"input": "", "expected": "8"}],
        },
    },

    # ── Lesson 8: Basic Metaprogramming ──────────────────────────────────────
    "les-advanced-python-8-beginner": {
        "title": "Introspection Basics",
        "content": """# Introspection Basics

## 🎯 Learning Objectives
- Use `dir()`, `type()`, and `id()` to inspect objects
- Check if an object has an attribute using `hasattr()`
- Get/Set attributes dynamically

## 📚 Concept Overview
Introspection is the ability of code to examine itself at runtime.

```python
x = 10
print(type(x)) # <class 'int'>
print(dir(x)) # List of all methods like __add__, etc.

if hasattr(x, "__add__"):
    print("Supports addition")
```

## 🏆 Key Takeaways
- `dir()` is the most useful tool for exploring unknown objects in the REPL.
""",
        "questions": [
            {"text": "Which function returns the unique ID of an object in memory?", "options": [
                {"text": "id()", "correct": True}, {"text": "self()", "correct": False},
                {"text": "memory()", "correct": False}, {"text": "uid()", "correct": False}]},
            {"text": "How do you check if an object 'obj' has a method named 'run'?", "options": [
                {"text": "hasattr(obj, 'run')", "correct": True},
                {"text": "obj.has('run')", "correct": False},
                {"text": "checkattr(obj, 'run')", "correct": False},
                {"text": "if 'run' in obj", "correct": False}]},
        ],
        "challenge": {
            "title": "Attr Checker",
            "description": "Print 'Yes' if string 'abc' has a method named `upper`, else 'No'.",
            "initial_code": "s = 'abc'\n# hasattr check\n",
            "solution_code": "s = 'abc'\nif hasattr(s, 'upper'): print('Yes')\nelse: print('No')\n",
            "test_cases": [{"input": "", "expected": "Yes"}],
        },
    },

    "les-advanced-python-8-intermediate": {
        "title": "Dynamic Class Creation (type)",
        "content": """# Dynamic Class Creation (type)

## 🎯 Learning Objectives
- Use the `type()` function to create classes on the fly
- Understand that `type` is actually a class
- Define methods for dynamic classes

## 📚 Concept Overview
Usually we use `class MyClass: ...`. But you can also do it programmatically.

```python
# type(name, bases, dict)
MyClass = type("MyClass", (object,), {"x": 5})

obj = MyClass()
print(obj.x) # 5
```

## 🏆 Key Takeaways
- In Python, classes are objects too. They are instances of the class `type`.
""",
        "questions": [
            {"text": "What are the three arguments taken by the `type()` class factory?", "options": [
                {"text": "name, bases (parents), and namespace dictionary", "correct": True},
                {"text": "id, name, value", "correct": False},
                {"text": "class, object, attribute", "correct": False},
                {"text": "module, file, function", "correct": False}]},
        ],
        "challenge": {
            "title": "Lazy Class",
            "description": "Use `type` to create a class named `A` with an attribute `active = True`. Instantiate it and print the attribute.",
            "initial_code": "# code with type()\n",
            "solution_code": "A = type('A', (), {'active': True})\nprint(A().active)\n",
            "test_cases": [{"input": "", "expected": "True"}],
        },
    },

    "les-advanced-python-8-pro": {
        "title": "Metaclasses Intro",
        "content": """# Metaclasses Intro

## 🎯 Learning Objectives
- Understand that Metaclasses are "Class Factories"
- Create a simple metaclass by inheriting from `type`
- Intercept class creation to enforce rules

## 📚 Concept Overview
A **Metaclass** is the "class of a class". It allows you to control how classes are created (not just objects).

```python
class UpperAttrMetaclass(type):
    def __new__(cls, name, bases, dct):
        # Enforce all attributes are uppercase
        return super().__new__(cls, name, bases, dct)
```

## 🏆 Key Takeaways
- "Metaclasses are deeper magic than 99% of users should ever worry about." (Tim Peters, inventor of Timsort).
""",
        "questions": [
            {"text": "True or False: A Metaclass is the class of a class.", "options": [
                {"text": "True", "correct": True}, {"text": "False", "correct": False}]},
        ],
        "challenge": {
            "title": "Magic Question",
            "description": "In Python, which built-in class is the base metaclass for all classes?",
            "initial_code": "# answer\n",
            "solution_code": "print('type')\n",
            "test_cases": [{"input": "", "expected": "type"}],
        },
    },

    # ── Lesson 9: Concurrency Intro ──────────────────────────────────────────
    "les-advanced-python-9-beginner": {
        "title": "Threads vs Processes",
        "content": """# Threads vs Processes

## 🎯 Learning Objectives
- Distinguish between I/O-bound and CPU-bound tasks
- Understand the Global Interpreter Lock (GIL)
- Pick the right tool for performance

## 📚 Concept Overview
- **Threads**: Shared memory. Good for waiting on networks/files (I/O).
- **Processes**: Separate memory. Good for heavy calculations (CPU).

### The GIL
CPython allows only one thread to execute Python bytecode at a time. This is why threads don't help much for heavy math, but are great for web scrapers.

## 🏆 Key Takeaways
- Use `threading` for web requests.
- Use `multiprocessing` for data processing.
""",
        "questions": [
            {"text": "What does GIL stand for?", "options": [
                {"text": "Global Interpreter Lock", "correct": True},
                {"text": "General Interface Library", "correct": False},
                {"text": "Global Internal Logic", "correct": False},
                {"text": "Generate Image Link", "correct": False}]},
            {"text": "Which module is better for tasks involving heavy mathematical computations?", "options": [
                {"text": "multiprocessing", "correct": True}, {"text": "threading", "correct": False},
                {"text": "sys", "correct": False}, {"text": "io", "correct": False}]},
        ],
        "challenge": {
            "title": "Concurrency Pick",
            "description": "If you are downloading 50 images from a website, which module should you use? Print 'threading' or 'multiprocessing'.",
            "initial_code": "# choice\n",
            "solution_code": "print('threading')\n",
            "test_cases": [{"input": "", "expected": "threading"}],
        },
    },

    "les-advanced-python-9-intermediate": {
        "title": "The threading Module",
        "content": """# The threading Module

## 🎯 Learning Objectives
- Create and start a thread
- Use `join()` to wait for completion
- Understand the `Target` parameter

## 📚 Concept Overview
```python
import threading
import time

def task():
    time.sleep(1)
    print("Finish")

t = threading.Thread(target=task)
t.start()
t.join() # Wait for it to finish!
```

## 🏆 Key Takeaways
- Always `join()` your threads if you need their results before continuing in the main program.
""",
        "questions": [
            {"text": "Which method is used to wait for a thread to finish its work?", "options": [
                {"text": "join()", "correct": True}, {"text": "wait()", "correct": False},
                {"text": "stop()", "correct": False}, {"text": "pause()", "correct": False}]},
        ],
        "challenge": {
            "title": "Thread Start",
            "description": "Write the two lines of code to start a thread `t` and then immediately wait for it to end.",
            "initial_code": "import threading\nt = threading.Thread(target=lambda: 1)\n# start and wait\n",
            "solution_code": "import threading\nt = threading.Thread(target=lambda: 1)\nt.start()\nt.join()\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-advanced-python-9-pro": {
        "title": "Queues & Thread Safety",
        "content": """# Queues & Thread Safety

## 🎯 Learning Objectives
- Use the `queue.Queue` for safe communication
- Understand the problem of "Race Conditions"
- Build a producer-consumer system

## 📚 Concept Overview
Threads share memory. If two threads try to change the same number at the exact same millisecond, the final count might be wrong. This is a **Race Condition**.

The `queue` module handles this safely using internal locks.

## 🏆 Key Takeaways
- Never share simple variables between threads without a `Lock` or a `Queue`.
""",
        "questions": [
            {"text": "What is it called when two threads modify a resource at the same time, leading to unpredictable results?", "options": [
                {"text": "Race Condition", "correct": True}, {"text": "Deadlock", "correct": False},
                {"text": "Segment Fault", "correct": False}, {"text": "Sync Error", "correct": False}]},
        ],
        "challenge": {
            "title": "Safety Tool",
            "description": "Name the object from the `threading` module used to ensure only one thread can access a block of code at a time.",
            "initial_code": "# answer\n",
            "solution_code": "print('Lock')\n",
            "test_cases": [{"input": "", "expected": "Lock"}],
        },
    },

    # ── Lesson 10: Mini Project ──────────────────────────────────────────────
    "les-advanced-python-10-beginner": {
        "title": "Project: List Processor",
        "content": """# Project: List Processor

## 🎯 Goal
Build a pipeline that squares numbers and filters those greater than 50.

## 📝 Features
- User input string of numbers.
- `map` and `filter` usage.
- Output final list.
""",
        "questions": [],
        "challenge": {
            "title": "Logic Pipeline",
            "description": "Given `nums = [1, 10, 20]`. Use `filter` and `map` to square them and return only those > 10. Print result.",
            "initial_code": "nums = [1, 10, 20]\n# process\n",
            "solution_code": "nums = [1, 10, 20]\nres = [x*x for x in nums if x*x > 10]\nprint(res)\n",
            "test_cases": [{"input": "", "expected": "[100, 400]"}],
        },
    },

    "les-advanced-python-10-intermediate": {
        "title": "Project: Performance Decorator",
        "content": """# Project: Performance Decorator

## 🎯 Goal
Write an `@time_it` decorator that prints how long a function took to execute.

## 📝 Features
- `time.time()`
- `*args` and `**kwargs` support.
- Prints 'Function X took Y seconds'.
""",
        "questions": [],
        "challenge": {
            "title": "Timer Wrapper",
            "description": "Write a decorator that prints 'GO' then the function result. Use a wrapper.",
            "initial_code": "def go_dec(f):\n    # implement wrapper\n",
            "solution_code": "def go_dec(f):\n    def wrapper(*a, **k):\n        print('GO')\n        return f(*a, **k)\n    return wrapper\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-advanced-python-10-pro": {
        "title": "Project: Dynamic Plugin Loader",
        "content": """# Project: Dynamic Plugin Loader

## 🎯 Goal
Build a system that finds `.py` files in a folder and dynamically imports them as "Plugins".

## 📝 Features
- `os.listdir()`
- `importlib.import_module()`
- Introspection to check if the plugin has a `run()` method.
""",
        "questions": [],
        "challenge": {
            "title": "Dynamic Check",
            "description": "Print 'Plugin OK' if an object `p` has a callable attribute `run`. Use `hasattr` and `callable`.",
            "initial_code": "# check p.run\n",
            "solution_code": "if hasattr(p, 'run') and callable(p.run): print('Plugin OK')\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },
}

class Command(BaseCommand):
    help = "Hydrate Module 9 (Advanced Python) — Lessons 6-10"

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
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Hydrated {count} lessons in Module 9 (6-10)"))
