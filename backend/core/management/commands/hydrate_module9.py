"""python manage.py hydrate_module9 -- Module 9 Advanced Python Lessons 1-5"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Lesson, Quiz, Question, Challenge

LESSONS = {
    # ── Lesson 1: List & Dict Comprehensions ──────────────────────────────────
    "les-advanced-python-1-beginner": {
        "title": "Mastering Comprehensions",
        "content": """# Mastering Comprehensions

## 🎯 Learning Objectives
- Write concise List, Set, and Dict comprehensions
- Use conditional logic (`if`) inside comprehensions
- Replace simple loops with comprehension syntax

## 📚 Concept Overview
Comprehensions provide a compact way to create collections.

```python
# List comprehension
squares = [x*x for x in range(10)]

# With condition
evens = [x for x in range(10) if x % 2 == 0]

# Dict comprehension
prices = {"apple": 0.5, "banana": 0.3}
discount = {k: v * 0.9 for k, v in prices.items()}
```

## 🏆 Key Takeaways
- Use comprehensions for readability, but don't over-nest them.
- They are generally faster than manual `for` loops in Python.
""",
        "questions": [
            {"text": "Which collection type is created by `{x: x*2 for x in range(5)}`?", "options": [
                {"text": "Dictionary", "correct": True}, {"text": "Set", "correct": False},
                {"text": "List", "correct": False}, {"text": "Tuple", "correct": False}]},
            {"text": "True or False: Comprehensions can include 'if' statements to filter data.", "options": [
                {"text": "True", "correct": True}, {"text": "False", "correct": False}]},
        ],
        "challenge": {
            "title": "Even Squares",
            "description": "Create a list of squares for all even numbers between 1 and 20 (inclusive) using a list comprehension. Print the list.",
            "initial_code": "# List comprehension here\n",
            "solution_code": "ls = [x*x for x in range(1, 21) if x % 2 == 0]\nprint(ls)\n",
            "test_cases": [{"input": "", "expected": "[4, 16, 36, 64, 100, 144, 196, 256, 324, 400]"}],
        },
    },

    "les-advanced-python-1-intermediate": {
        "title": "Nested Comprehensions",
        "content": """# Nested Comprehensions

## 🎯 Learning Objectives
- Flatten nested lists using comprehensions
- Create 2D matrices
- Handle complex data transformation

## 📚 Concept Overview
You can put a comprehension inside another, or use multiple `for` clauses.

```python
# Flattening a 2D list
matrix = [[1, 2], [3, 4]]
flat = [num for row in matrix for num in row] # [1, 2, 3, 4]

# Creating a 3x3 grid
grid = [[0 for _ in range(3)] for _ in range(3)]
```

## ⚠️ Common Pitfalls
- **Readability**: If your comprehension has more than 2 `for` clauses, it's usually better to use a standard loop.

## 🏆 Key Takeaways
- Nested comprehensions are powerful for data preprocessing in Data Science.
""",
        "questions": [
            {"text": "In `[attr for item in list for attr in item]`, which loop runs first?", "options": [
                {"text": "for item in list", "correct": True},
                {"text": "for attr in item", "correct": False},
                {"text": "They run in parallel", "correct": False},
                {"text": "The inner one", "correct": False}]},
        ],
        "challenge": {
            "title": "Flatten Master",
            "description": "Given `data = [[1], [2, 3], [4]]`, use a single comprehension to flatten it into `[1, 2, 3, 4]`. Print the result.",
            "initial_code": "data = [[1], [2, 3], [4]]\n# Flatten it\n",
            "solution_code": "data = [[1], [2, 3], [4]]\nprint([x for sub in data for x in sub])\n",
            "test_cases": [{"input": "", "expected": "[1, 2, 3, 4]"}],
        },
    },

    "les-advanced-python-1-pro": {
        "title": "Performance: Loops vs Comprehensions",
        "content": """# Performance: Loops vs Comprehensions

## 🎯 Learning Objectives
- Use the `timeit` module to compare speeds
- Understand CPython's bytecode optimization for comprehensions
- Choose the best tool for high-performance loops

## 📚 Concept Overview
Comprehensions are executed at C-level speeds within the Python interpreter, avoiding some of the overhead of regular `for` loop lookups.

```python
import timeit
# Compare speeds of create a list of 1M items
```

## 🏆 Key Takeaways
- For simple list creation, comprehensions are ~10-20% faster than `.append()`.
- Use them for performance AND clarity.
""",
        "questions": [
            {"text": "Why are comprehensions generally faster than manual loops with .append()?", "options": [
                {"text": "They are optimized at the bytecode level and avoid multiple attribute lookups", "correct": True},
                {"text": "They use multi-threading automatically", "correct": False},
                {"text": "They skip integer validation", "correct": False},
                {"text": "They are pre-compiled by the OS", "correct": False}]},
        ],
        "challenge": {
            "title": "Speed Choice",
            "description": "Which is faster for creating a list of 1000 items from a range: `list(range(1000))` or `[x for x in range(1000)]`? Print 'CONVERT' or 'COMP'.",
            "initial_code": "# Choice\n",
            "solution_code": "print('CONVERT')\n",
            "test_cases": [{"input": "", "expected": "CONVERT"}],
        },
    },

    # ── Lesson 2: Generators & Yield ─────────────────────────────────────────
    "les-advanced-python-2-beginner": {
        "title": "Introduction to Generators",
        "content": """# Introduction to Generators

## 🎯 Learning Objectives
- Use `yield` to create generator functions
- Understand "Lazy Evaluation" (saving memory)
- Use `next()` to pull values

## 📚 Concept Overview
A regular function `return`s once and exits. A **Generator** `yield`s a value, pauses, and remembers its state.

```python
def count_to_three():
    yield 1
    yield 2
    yield 3

gen = count_to_three()
print(next(gen)) # 1
print(next(gen)) # 2
```

## 🏆 Key Takeaways
- Generators don't store the whole list in memory; they calculate items on demand.
- Great for processing huge files (Giga-bytes) line-by-line.
""",
        "questions": [
            {"text": "Which keyword makes a function a generator?", "options": [
                {"text": "yield", "correct": True}, {"text": "return", "correct": False},
                {"text": "gen", "correct": False}, {"text": "provide", "correct": False}]},
            {"text": "What happens when a generator function is called?", "options": [
                {"text": "It returns a generator object without running any code yet", "correct": True},
                {"text": "It runs the whole function and returns a list", "correct": False},
                {"text": "It crashes", "correct": False},
                {"text": "It creates a new thread", "correct": False}]},
        ],
        "challenge": {
            "title": "Simple Generator",
            "description": "Write a generator function `odds(n)` that yields odd numbers from 1 to `n`. Loop through `odds(5)` and print them.",
            "initial_code": "def odds(n):\n    # yield odd numbers\n",
            "solution_code": "def odds(n):\n    for i in range(1, n+1):\n        if i % 2 != 0: yield i\nfor val in odds(5):\n    print(val)\n",
            "test_cases": [{"input": "", "expected": "1\n3\n5"}],
        },
    },

    "les-advanced-python-2-intermediate": {
        "title": "Generator Expressions",
        "content": """# Generator Expressions

## 🎯 Learning Objectives
- Write one-line generators using `()`
- Compare memory usage with list comprehensions
- Use generators as function arguments

## 📚 Concept Overview
Generator expressions look like list comprehensions but use parentheses `()`.

```python
# List (Takes 8MB RAM for 1M items)
ls = [x for x in range(1000000)]

# Generator (Takes ~100 bytes RAM)
ge = (x for x in range(1000000))
```

## 🏆 Key Takeaways
- Use list comprehensions `[]` if you need to access items multiple times.
- Use generator expressions `()` if you only need to iterate through them once.
""",
        "questions": [
            {"text": "What syntax defines a generator expression?", "options": [
                {"text": "(x for x in data)", "correct": True},
                {"text": "[x for x in data]", "correct": False},
                {"text": "{x for x in data}", "correct": False},
                {"text": "yield x for x in data", "correct": False}]},
        ],
        "challenge": {
            "title": "Memory Champ",
            "description": "Create a generator expression for squares of numbers 1-100. Sum them up using the `sum()` function and print the total.",
            "initial_code": "# code here\n",
            "solution_code": "sq_gen = (x*x for x in range(1, 101))\nprint(sum(sq_gen))\n",
            "test_cases": [{"input": "", "expected": "338350"}],
        },
    },

    "les-advanced-python-2-pro": {
        "title": "Advanced Generator Methods (send, close)",
        "content": """# Advanced Generator Methods (send, close)

## 🎯 Learning Objectives
- Pass data BACK into a generator using `.send()`
- Stop a generator manually with `.close()`
- Create bi-directional coroutines

## 📚 Concept Overview
Generators aren't just for output! You can send data into them.

```python
def printer():
    while True:
        val = yield # execution stops here, waits for 'send'
        print(f"Received: {val}")

p = printer()
next(p) # 'Prime' the generator
p.send("Hello") # Received: Hello
```

## 🏆 Key Takeaways
- `.send()` is the foundation for asynchronous programming and task schedulers in Python.
""",
        "questions": [
            {"text": "Which method allows you to pass a value back into a generator?", "options": [
                {"text": "send()", "correct": True}, {"text": "input()", "correct": False},
                {"text": "push()", "correct": False}, {"text": "write()", "correct": False}]},
        ],
        "challenge": {
            "title": "The Send Trap",
            "description": "True or False: You must call `next()` on a generator at least once before you can use `.send()` with a non-None value.",
            "initial_code": "# True or False?\n",
            "solution_code": "print('True')\n",
            "test_cases": [{"input": "", "expected": "True"}],
        },
    },

    # ── Lesson 3: Iterators ──────────────────────────────────────────────────
    "les-advanced-python-3-beginner": {
        "title": "The Iterator Protocol",
        "content": """# The Iterator Protocol

## 🎯 Learning Objectives
- Differentiate between **Iterable** and **Iterator**
- Use `iter()` and `next()` manually
- Understand the internal mechanics of a `for` loop

## 📚 Concept Overview
- **Iterable**: Any object you can loop over (List, String, Range).
- **Iterator**: The actual "pointer" that moves through the items.

```python
numbers = [1, 2]
it = iter(numbers) # Get iterator

print(next(it)) # 1
print(next(it)) # 2
# print(next(it)) # Raises StopIteration
```

## 🏆 Key Takeaways
- All iterators are iterables, but not all iterables are iterators.
""",
        "questions": [
            {"text": "What exception is raised when an iterator has no more items?", "options": [
                {"text": "StopIteration", "correct": True}, {"text": "IndexError", "correct": False},
                {"text": "EOFError", "correct": False}, {"text": "FinishError", "correct": False}]},
        ],
        "challenge": {
            "title": "Manual Step",
            "description": "Given `data = [10, 20]`, manually create an iterator and print the second element using `next()` twice.",
            "initial_code": "data = [10, 20]\n# print 20\n",
            "solution_code": "data = [10, 20]\nit = iter(data)\nnext(it)\nprint(next(it))\n",
            "test_cases": [{"input": "", "expected": "20"}],
        },
    },

    "les-advanced-python-3-intermediate": {
        "title": "Custom Iterators",
        "content": """# Custom Iterators

## 🎯 Learning Objectives
- Implement `__iter__` and `__next__` in your own classes
- Build objects that can be used in `for` loops
- Control exact step-by-step logic

## 📚 Concept Overview
```python
class PowerOfTwo:
    def __init__(self, max_p): self.max, self.n = max_p, 0
    
    def __iter__(self): return self

    def __next__(self):
        if self.n > self.max: raise StopIteration
        res = 2 ** self.n
        self.n += 1
        return res
```

## 🏆 Key Takeaways
- Implementing the protocol allows your custom objects to integrate perfectly with the language (looping, map, filter, etc.).
""",
        "questions": [
            {"text": "Which two methods must a class implement to be a proper iterator?", "options": [
                {"text": "__iter__ and __next__", "correct": True},
                {"text": "__start__ and __end__", "correct": False},
                {"text": "__get__ and __set__", "correct": False},
                {"text": "__loop__ and __item__", "correct": False}]},
        ],
        "challenge": {
            "title": "Infinite Count",
            "description": "Implement a class `Counter` that yields 1, 2, 3... forever. Print the result of `next()` on its instance twice.",
            "initial_code": "# Class with __next__\n",
            "solution_code": "class Counter:\n    def __init__(self): self.n = 1\n    def __iter__(self): return self\n    def __next__(self): \n        res = self.n; self.n += 1; return res\nc = Counter()\nprint(next(c))\nprint(next(c))\n",
            "test_cases": [{"input": "", "expected": "1\n2"}],
        },
    },

    "les-advanced-python-3-pro": {
        "title": "Infinite Iterators (itertools)",
        "content": """# Infinite Iterators (itertools)

## 🎯 Learning Objectives
- Master the `itertools` library
- Use `count()`, `cycle()`, and `repeat()`
- Handle high-level data pipelines

## 📚 Concept Overview
`itertools` contains specialized iterators written in C.

```python
import itertools

# numbers: 10, 11, 12...
for n in itertools.count(10):
    if n > 12: break
    print(n)
```

## 🏆 Key Takeaways
- `itertools` is the gold standard for efficient looping and combinations.
""",
        "questions": [
            {"text": "Which method from `itertools` repeats a sequence forever? (e.g. A, B, A, B...)", "options": [
                {"text": "cycle()", "correct": True}, {"text": "repeat()", "correct": False},
                {"text": "forever()", "correct": False}, {"text": "loop()", "correct": False}]},
        ],
        "challenge": {
            "title": "Cycle Pick",
            "description": "Assume `itertools.cycle([1, 2])`. Print the first 3 values it would yield (space separated).",
            "initial_code": "# 1 2 ...\n",
            "solution_code": "print('1 2 1')\n",
            "test_cases": [{"input": "", "expected": "1 2 1"}],
        },
    },

    # ── Lesson 4: Decorators ─────────────────────────────────────────────────
    "les-advanced-python-4-beginner": {
        "title": "Function Wrappers",
        "content": """# Function Wrappers

## 🎯 Learning Objectives
- Understand that functions are "First-Class Objects"
- Create a function that takes another function as an argument
- The goal of decorators: Add logic WITHOUT changing the source code

## 📚 Concept Overview
A decorator is like a wrapper around a gift. It extends behavior without touching the gift itself.

```python
def my_decorator(func):
    def wrapper():
        print("Something before")
        func()
        print("Something after")
    return wrapper

@my_decorator
def say_hi(): print("Hi!")
```

## 🏆 Key Takeaways
- `@name` is just syntax for `func = name(func)`.
""",
        "questions": [
            {"text": "What is the @ symbol called in the context of Python functions?", "options": [
                {"text": "A decorator", "correct": True}, {"text": "A wrapper", "correct": False},
                {"text": "An annotation", "correct": False}, {"text": "An at-attribute", "correct": False}]},
            {"text": "What does a decorator essentially do?", "options": [
                {"text": "Modifies or extends the behavior of a function without permanently changing it", "correct": True},
                {"text": "Deletes the function from memory", "correct": False},
                {"text": "Compiles the function into C code", "correct": False},
                {"text": "Calculates the function's return value", "correct": False}]},
        ],
        "challenge": {
            "title": "Bold Text",
            "description": "Write a decorator `bold(func)` that prints '***' before and after calling the function.",
            "initial_code": "def bold(func):\n    # write wrapper\n",
            "solution_code": "def bold(func):\n    def wrapper():\n        print('***')\n        func()\n        print('***')\n    return wrapper\n@bold\ndef hi(): print('HI')\nhi()\n",
            "test_cases": [{"input": "", "expected": "***\nHI\n***"}],
        },
    },

    "les-advanced-python-4-intermediate": {
        "title": "Decorators with Arguments (*args, **kwargs)",
        "content": """# Decorators with Arguments (*args, **kwargs)

## 🎯 Learning Objectives
- Build decorators that work with any function signature
- Pass parameters into the decorator itself
- Use `functools.wraps` to preserve metadata

## 📚 Concept Overview
```python
import functools

def logger(func):
    @functools.wraps(func) # Fixes __name__ and __doc__
    def wrapper(*args, **kwargs):
        print(f"Calling with {args}")
        return func(*args, **kwargs)
    return wrapper
```

## 🏆 Key Takeaways
- Always use `@functools.wraps` in your wrappers so you don't "lose" your function's identity (name, docs).
""",
        "questions": [
            {"text": "Why should you use `@functools.wraps(func)` inside your decorator?", "options": [
                {"text": "To preserve the original function's name and docstring", "correct": True},
                {"text": "To make it faster", "correct": False},
                {"text": "To allow external imports", "correct": False},
                {"text": "To encrypt the wrapper", "correct": False}]},
        ],
        "challenge": {
            "title": "Global Logger",
            "description": "Write a wrapper that prints the first argument passed to the function, then returns the function result.",
            "initial_code": "def log_first(func):\n    def wrapper(*args, **kwargs):\n        # print args[0]\n",
            "solution_code": "def log_first(func):\n    def wrapper(*args, **kwargs):\n        print(args[0])\n        return func(*args, **kwargs)\n    return wrapper\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-advanced-python-4-pro": {
        "title": "Class Decorators & Multiple Decorators",
        "content": """# Class Decorators & Multiple Decorators

## 🎯 Learning Objectives
- Use a class as a decorator (implementing `__call__`)
- Stack multiple decorators on a single function
- Understand the "Top-Down" execution order

## 📚 Concept Overview
```python
@decorator_two # Runs second
@decorator_one # Runs first
def my_func(): pass
```

### Class Decorator
```python
class CountCalls:
    def __init__(self, func):
        self.func, self.num = func, 0
    def __call__(self, *args, **kwargs):
        self.num += 1
        return self.func(*args, **kwargs)
```

## 🏆 Key Takeaways
- Decorators are just "Function Factories". You can chain them to build complex behavior.
""",
        "questions": [
            {"text": "In what order are stacked decorators executed?", "options": [
                {"text": "Top to bottom (the closest one to function runs first)", "correct": False},
                {"text": "Bottom up (the one just above the def runs first)", "correct": True},
                {"text": "Random order", "correct": False},
                {"text": "Alphabetical order", "correct": False}]},
        ],
        "challenge": {
            "title": "Call Tracker",
            "description": "Which magic method must a class implement to be used as a decorator?",
            "initial_code": "# __??__\n",
            "solution_code": "print('__call__')\n",
            "test_cases": [{"input": "", "expected": "__call__"}],
        },
    },

    # ── Lesson 5: Scoping & Closures ─────────────────────────────────────────
    "les-advanced-python-5-beginner": {
        "title": "Local vs Global Scope",
        "content": """# Local vs Global Scope

## 🎯 Learning Objectives
- Understand the LEGB rule (Local, Enclosing, Global, Built-in)
- Use the `global` keyword (sparingly!)
- Avoid naming collisions

## 📚 Concept Overview
Python looks for variables in this order:
1. **L**ocal: Inside current function.
2. **E**nclosing: In outer functions (for nested).
3. **G**lobal: At top level of script.
4. **B**uilt-in: Python's core (len, range).

```python
x = 10 # Global
def f():
    global x
    x = 20 # Changes the global x!
```

## 🏆 Key Takeaways
- Be careful with `global`. It's usually better to pass arguments and return values.
""",
        "questions": [
            {"text": "What does the 'E' in LEGB stand for?", "options": [
                {"text": "Enclosing", "correct": True}, {"text": "External", "correct": False},
                {"text": "Error", "correct": False}, {"text": "Everything", "correct": False}]},
            {"text": "Which keyword allows you to modify a variable defined at the top level of your script from inside a function?", "options": [
                {"text": "global", "correct": True}, {"text": "outer", "correct": False},
                {"text": "top", "correct": False}, {"text": "access", "correct": False}]},
        ],
        "challenge": {
            "title": "Global Fix",
            "description": "Define `counter = 0`. Write a function `inc()` that uses the `global` keyword to add 1 to `counter`.",
            "initial_code": "counter = 0\ndef inc():\n    # fix the counter\n",
            "solution_code": "counter = 0\ndef inc():\n    global counter\n    counter += 1\ninc()\nprint(counter)\n",
            "test_cases": [{"input": "", "expected": "1"}],
        },
    },

    "les-advanced-python-5-intermediate": {
        "title": "Closures Explained",
        "content": """# Closures Explained

## 🎯 Learning Objectives
- Define a "Closure" (Nested function remembering outer state)
- Use closures for data encapsulation
- Create simple stateful functions

## 📚 Concept Overview
A closure happens when a nested function references a variable from its outer scope, and the outer function has finished execution.

```python
def make_multiplier(n):
    def multiply(x):
        return x * n # n is "remembered"
    return multiply

times3 = make_multiplier(3)
print(times3(10)) # 30
```

## 🏆 Key Takeaways
- Closures are a great alternative to simple classes with only one method.
""",
        "questions": [
            {"text": "What is a closure?", "options": [
                {"text": "A nested function that retains access to variables from its parent function's scope", "correct": True},
                {"text": "A function that has been deleted", "correct": False},
                {"text": "A function with no return value", "correct": False},
                {"text": "A class with no methods", "correct": False}]},
        ],
        "challenge": {
            "title": "Multiplier Factory",
            "description": "Create a function `make_adder(n)` that returns a function which adds `n` to its input. Call `add10 = make_adder(10)` and print `add10(5)`.",
            "initial_code": "# Closures\n",
            "solution_code": "def make_adder(n):\n    def adder(x): return x + n\n    return adder\nadd10 = make_adder(10)\nprint(add10(5))\n",
            "test_cases": [{"input": "", "expected": "15"}],
        },
    },

    "les-advanced-python-5-pro": {
        "title": "Nonlocal & State Persistence",
        "content": """# Nonlocal & State Persistence

## 🎯 Learning Objectives
- Use the `nonlocal` keyword to modify enclosing variables
- Build counters without global variables
- Understand the difference between `global` and `nonlocal`

## 📚 Concept Overview
`global` refers to the top-level script. `nonlocal` refers to the **nearest** outer function.

```python
def parent():
    count = 0
    def child():
        nonlocal count
        count += 1
        return count
    return child
```

## 🏆 Key Takeaways
- `nonlocal` is essential for creating "Private" stateful functions in closures.
""",
        "questions": [
            {"text": "Which keyword is used to modify a variable in the 'Enclosing' scope of a nested function?", "options": [
                {"text": "nonlocal", "correct": True}, {"text": "global", "correct": False},
                {"text": "parent", "correct": False}, {"text": "outer", "correct": False}]},
        ],
        "challenge": {
            "title": "Private Counter",
            "description": "Use `nonlocal` inside a nested function `step()` to increment a variable `val` from the outer function `tracker()`. Return `step`.",
            "initial_code": "def tracker():\n    val = 0\n    def step():\n        # nonlocal logic\n",
            "solution_code": "def tracker():\n    val = 0\n    def step():\n        nonlocal val\n        val += 1\n        return val\n    return step\ns = tracker()\nprint(s())\nprint(s())\n",
            "test_cases": [{"input": "", "expected": "1\n2"}],
        },
    },
}

class Command(BaseCommand):
    help = "Hydrate Module 9 (Advanced Python) — Lessons 1-5"

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
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Hydrated {count} lessons in Module 9 (1-5)"))
