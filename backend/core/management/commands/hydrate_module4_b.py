"""python manage.py hydrate_module4_b -- Module 4 Functions Lessons 6-10"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Lesson, Quiz, Question, Challenge

LESSONS = {
    # ── Lesson 6: *args and **kwargs ─────────────────────────────────────────
    "les-functions-6-beginner": {
        "title": "Arbitrary Arguments (*args)",
        "content": """# Arbitrary Arguments (*args)

## 🎯 Learning Objectives
- Use `*args` to accept any number of positional arguments
- Understand how `*args` packs values into a tuple
- Loop through arbitrary arguments efficiently

## 📚 Concept Overview
Sometimes you don't know how many arguments will be passed into your function. `*args` (the star is the important part) allows you to handle this.

```python
def my_sum(*args):
    return sum(args) # args is a tuple

print(my_sum(1, 2, 3))    # 6
print(my_sum(10, 20))      # 30
```

## 🏆 Key Takeaways
- The name `args` is a convention, but the `*` symbol is required.
- `args` is received as a **tuple** inside the function.
- It's useful for functions like `print()` or math aggregators.
""",
        "questions": [
            {"text": "What type of object is `args` inside a function defined as `def func(*args):`?", "options": [
                {"text": "Tuple", "correct": True}, {"text": "List", "correct": False},
                {"text": "Dictionary", "correct": False}, {"text": "Set", "correct": False}]},
            {"text": "Which character allows a function to accept any number of positional arguments?", "options": [
                {"text": "*", "correct": True}, {"text": "**", "correct": False},
                {"text": "&", "correct": False}, {"text": "@", "correct": False}]},
        ],
        "challenge": {
            "title": "Multiplier Pro",
            "description": "Define a function `multiply_all(*args)` that return the product of all numbers passed to it. If no arguments, return 1.",
            "initial_code": "# Use *args\n",
            "solution_code": "def multiply_all(*args):\n    res = 1\n    for n in args:\n        res *= n\n    return res\nprint(multiply_all(2, 3, 4))\n",
            "test_cases": [{"input": "", "expected": "24"}],
        },
    },

    "les-functions-6-intermediate": {
        "title": "Keyword Arbitrary Arguments (**kwargs)",
        "content": """# Keyword Arbitrary Arguments (**kwargs)

## 🎯 Learning Objectives
- Use `**kwargs` to accept any number of keyword arguments
- Access values in `kwargs` using dictionary methods
- Mix `*args` and `**kwargs` correctly

## 📚 Concept Overview
`**kwargs` allows you to pass as many keyword arguments as you want. They are received as a **dictionary**.

```python
def print_user(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_user(name="Alice", age=25, job="Dev")
```

### Mixing order
1. Positional
2. `*args`
3. Optional (defaults)
4. `**kwargs`

## 🏆 Key Takeaways
- `kwargs` is a dictionary inside the function.
- It's great for passing configurations or metadata.
""",
        "questions": [
            {"text": "What type of object is `kwargs` inside a function?", "options": [
                {"text": "Dictionary", "correct": True}, {"text": "Tuple", "correct": False},
                {"text": "Json", "correct": False}, {"text": "Object", "correct": False}]},
        ],
        "challenge": {
            "title": "Builder Bot",
            "description": "Define `describe(**kwargs)`. It should print strings like 'key is value' for each pair. Call with brand='Tesla', model='S'.",
            "initial_code": "# Use **kwargs\n",
            "solution_code": "def describe(**kwargs):\n    for k, v in kwargs.items():\n        print(f'{k} is {v}')\ndescribe(brand='Tesla', model='S')\n",
            "test_cases": [{"input": "", "expected": "brand is Tesla\nmodel is S"}],
        },
    },

    "les-functions-6-pro": {
        "title": "Argument Unpacking",
        "content": """# Argument Unpacking

## 🎯 Learning Objectives
- Use `*` and `**` to unpack lists and dicts into function calls
- Bridge the gap between data structures and function parameters
- Optimize code that forwards arguments to other functions

## 📚 Concept Overview
You can use the same symbols to "explode" a collection into a function call.

```python
def add(a, b, c):
    return a + b + c

nums = [1, 2, 3]
# Instead of add(nums[0], nums[1], nums[2]):
print(add(*nums))

user_data = {"a": 10, "b": 20, "c": 30}
print(add(**user_data))
```

## 🏆 Key Takeaways
- Unpacking is the reverse of packing.
- It makes your code extremely flexible when working with dynamic data.
""",
        "questions": [
            {"text": "Which operator is used to unpack a dictionary into keyword arguments?", "options": [
                {"text": "**", "correct": True}, {"text": "*", "correct": False},
                {"text": "unpack()", "correct": False}, {"text": "%", "correct": False}]},
        ],
        "challenge": {
            "title": "Exploding Tuple",
            "description": "You are given a function `sum3(a, b, c)` that prints their sum. You are given a tuple `t = (5, 10, 15)`. Call `sum3` using unpacking.",
            "initial_code": "def sum3(a, b, c): print(a+b+c)\nt = (5, 10, 15)\n# Call here\n",
            "solution_code": "def sum3(a, b, c): print(a+b+c)\nt = (5, 10, 15)\nsum3(*t)\n",
            "test_cases": [{"input": "", "expected": "30"}],
        },
    },

    # ── Lesson 7: Lambda Functions ───────────────────────────────────────────
    "les-functions-7-beginner": {
        "title": "Lambda — Anonymous Functions",
        "content": """# Lambda — Anonymous Functions

## 🎯 Learning Objectives
- Define short functions in a single line
- Understand the syntax `lambda arguments: expression`
- Know when to use lambdas instead of `def`

## 📚 Concept Overview
Lambdas are small, one-line functions that don't have a name.

```python
# Standard
def add(x, y): return x + y

# Lambda
add_lambda = lambda x, y: x + y

print(add_lambda(5, 10)) # 15
```

## ⚠️ Common Pitfalls
- Overusing lambdas for complex logic. If it takes more than one line, use `def`.
- Forgetting that lambdas can only contain a **single expression**.

## 🏆 Key Takeaways
- Lambdas are "throwaway" functions often used as arguments to other functions.
- Syntax: `lambda x: x * 2` (no `return` keyword needed).
""",
        "questions": [
            {"text": "How many expressions can a lambda function contain?", "options": [
                {"text": "One", "correct": True}, {"text": "Three", "correct": False},
                {"text": "As many as needed", "correct": False}, {"text": "Zero", "correct": False}]},
            {"text": "Do you need the `return` keyword inside a lambda?", "options": [
                {"text": "No, it returns the result of the expression automatically", "correct": True},
                {"text": "Yes", "correct": False},
                {"text": "Only for strings", "correct": False},
                {"text": "Only if using parentheses", "correct": False}]},
        ],
        "challenge": {
            "title": "Quick Double",
            "description": "Create a lambda function named `double` that takes `x` and returns `x * 2`. Print `double(10)`.",
            "initial_code": "# Create and call lambda\n",
            "solution_code": "double = lambda x: x * 2\nprint(double(10))\n",
            "test_cases": [{"input": "", "expected": "20"}],
        },
    },

    "les-functions-7-intermediate": {
        "title": "Sorting with Lambdas",
        "content": """# Sorting with Lambdas

## 🎯 Learning Objectives
- Use lambdas as "keys" for sorting
- Sort complex data structures (like lists of tuples or dicts)
- Apply custom sorting logic efficiently

## 📚 Concept Overview
Sorting by a specific field is the most common use of lambdas.

```python
pairs = [(1, "one"), (3, "three"), (2, "two")]
# Sort by the word (second item) instead of number
sorted_pairs = sorted(pairs, key=lambda p: p[1])
# [(1, 'one'), (3, 'three'), (2, 'two')] -> (2, 'two') comes last alpha... etc.
```

## 🏆 Key Takeaways
- The `key` parameter in `sorted()` and `.sort()` accepts a function.
- Lambdas provide a lightweight way to define these transformation functions.
""",
        "questions": [
            {"text": "What is the purpose of the `key` parameter in the `sorted()` function?", "options": [
                {"text": "To define a function that extracts the comparison basis", "correct": True},
                {"text": "To provide a password for the data", "correct": False},
                {"text": "To specify the sorting algorithm", "correct": False},
                {"text": "To reverse the order", "correct": False}]},
        ],
        "challenge": {
            "title": "Sort by Length",
            "description": "Read a list of words. Sort them by their length (shortest to longest) using `sorted()` and a lambda. Print the result list.",
            "initial_code": "# Use sorted(words, key=...)\n",
            "solution_code": "words = input().split()\nres = sorted(words, key=lambda w: len(w))\nprint(res)\n",
            "test_cases": [{"input": "python is great language", "expected": "['is', 'great', 'python', 'language']"}],
        },
    },

    "les-functions-7-pro": {
        "title": "Lambdas vs Def (Internal Bytecode)",
        "content": """# Lambdas vs Def (Internal Bytecode)

## 🎯 Learning Objectives
- Compare performance of lambdas and def functions
- Understand how Python treats both internally
- Discuss best practices for debuggability

## 📚 Concept Overview
Internally, a lambda is almost identical to a `def` function. It generates a function object in memory.

### The Big Difference: Tracebacks
When a `def` function fails, the error message shows the **name** of the function.
When a lambda fails, it just says **<lambda>**, which is harder to debug in large call stacks.

## 🏆 Key Takeaways
- Use `def` for anything you might want to debug later.
- Use `lambda` for truly anonymous, simple operations.
""",
        "questions": [
            {"text": "What is a major disadvantage of using lambdas in complex code?", "options": [
                {"text": "Worse traceback messages for debugging", "correct": True}, {"text": "They are slower", "correct": False},
                {"text": "They use more memory", "correct": False}, {"text": "They can't access global variables", "correct": False}]},
        ],
        "challenge": {
            "title": "Lambda Conditional",
            "description": "Create a lambda that returns 'Even' if `x % 2 == 0` else 'Odd'. Print results for 4 and 7.",
            "initial_code": "# Lambda with ternary logic\n",
            "solution_code": "check = lambda x: 'Even' if x % 2 == 0 else 'Odd'\nprint(check(4))\nprint(check(7))\n",
            "test_cases": [{"input": "", "expected": "Even\nOdd"}],
        },
    },

    # ── Lesson 8: High-Order Functions ───────────────────────────────────────
    "les-functions-8-beginner": {
        "title": "Map & Filter",
        "content": """# Map & Filter

## 🎯 Learning Objectives
- Transform sequences using `map()`
- Filter sequences using `filter()`
- Convert results back to lists or tuples

## 📚 Concept Overview
High-order functions are functions that take other functions as arguments.

### map(func, iterable)
Applies `func` to every item.
```python
nums = [1, 2, 3]
squares = list(map(lambda x: x*x, nums)) # [1, 4, 9]
```

### filter(func, iterable)
Keeps items where `func(item)` is True.
```python
evens = list(filter(lambda x: x % 2 == 0, range(10)))
```

## 🏆 Key Takeaways
- `map` and `filter` return an **iterator**, so you usually wrap them in `list()`.
""",
        "questions": [
            {"text": "What does `map()` return by default?", "options": [
                {"text": "An iterator", "correct": True}, {"text": "A list", "correct": False},
                {"text": "A generator object", "correct": False}, {"text": "A tuple", "correct": False}]},
            {"text": "Which function is used to select elements based on a condition?", "options": [
                {"text": "filter", "correct": True}, {"text": "map", "correct": False},
                {"text": "reduce", "correct": False}, {"text": "sort", "correct": False}]},
        ],
        "challenge": {
            "title": "Word Length Filter",
            "description": "Read a list of words. Use `filter` and a lambda to keep only words with more than 3 characters. Print the result list.",
            "initial_code": "# Use filter\n",
            "solution_code": "words = input().split()\nres = list(filter(lambda w: len(w) > 3, words))\nprint(res)\n",
            "test_cases": [{"input": "cat dog bird elephant", "expected": "['bird', 'elephant']"}],
        },
    },

    "les-functions-8-intermediate": {
        "title": "Reduce & Partial Functions",
        "content": """# Reduce & Partial Functions

## 🎯 Learning Objectives
- Use `functools.reduce` for rolling computations
- Use `functools.partial` to "pre-fill" function arguments
- Understand the "Functional Programming" style in Python

## 📚 Concept Overview
### reduce()
Works by applying a function cumulatively to items.
```python
from functools import reduce
nums = [1, 2, 3, 4]
# ((1*2)*3)*4
product = reduce(lambda x, y: x * y, nums) # 24
```

### partial()
Creates a new version of a function with some arguments set.
```python
from functools import partial
def power(base, exp): return base ** exp
square = partial(power, exp=2)
print(square(10)) # 100
```

## 🏆 Key Takeaways
- `reduce` is no longer a built-in (must import from `functools`).
- `partial` is great for creating specialized versions of generic functions.
""",
        "questions": [
            {"text": "Where is the `reduce` function located in Python 3?", "options": [
                {"text": "functools", "correct": True}, {"text": "Built-ins", "correct": False},
                {"text": "itertools", "correct": False}, {"text": "math", "correct": False}]},
        ],
        "challenge": {
            "title": "Partial Adder",
            "description": "From `functools` import `partial`. Use it to create `add5` from a function `add(a, b)`. Print `add5(10)`.",
            "initial_code": "from functools import partial\ndef add(a, b): return a + b\n# Use partial\n",
            "solution_code": "from functools import partial\ndef add(a, b): return a + b\nadd5 = partial(add, b=5)\nprint(add5(10))\n",
            "test_cases": [{"input": "", "expected": "15"}],
        },
    },

    "les-functions-8-pro": {
        "title": "Writing Your Own High-Order Functions",
        "content": """# Writing Your Own High-Order Functions

## 🎯 Learning Objectives
- Pass one function into another
- Understand the "Strategy Pattern"
- Build flexible systems that accept plugins/behaviors

## 📚 Concept Overview
```python
def apply_operation(val, operation):
    \"\"\"Accepts a value and a function, and applies it.\"\"\"
    return operation(val)

print(apply_operation(10, lambda x: x * 5))
```

## 🏆 Key Takeaways
- Highly reusable code often allows the user to suggest the logic as a function parameter.
""",
        "questions": [
            {"text": "A function that takes another function as an argument is called:", "options": [
                {"text": "A high-order function", "correct": True}, {"text": "A meta-function", "correct": False},
                {"text": "A nested function", "correct": False}, {"text": "A super-function", "correct": False}]},
        ],
        "challenge": {
            "title": "Custom Runner",
            "description": "Define `run_twice(func, val)` that returns `func(func(val))`. Use it to double a number twice. Input: 5, Output: 20.",
            "initial_code": "# Define run_twice\n",
            "solution_code": "def run_twice(func, val):\n    return func(func(val))\nprint(run_twice(lambda x: x*2, 5))\n",
            "test_cases": [{"input": "", "expected": "20"}],
        },
    },

    # ── Lesson 9: Recursion Basics ───────────────────────────────────────────
    "les-functions-9-beginner": {
        "title": "Introduction to Recursion",
        "content": """# Introduction to Recursion

## 🎯 Learning Objectives
- Understand that a function can call itself
- Identify the "Base Case" and "Recursive Case"
- Avoid the "maximum recursion depth exceeded" error

## 📚 Concept Overview
Recursion is when a function calls itself to solve a smaller version of the same problem.

### The Two Laws of Recursion
1. **Base Case**: The condition that stops the recursion.
2. **Recursive Step**: Calling the function with a modified (smaller) input.

```python
def factorial(n):
    if n == 1: # Base Case
        return 1
    return n * factorial(n - 1) # Recursive Step
```

## ⚠️ Common Pitfalls
- Forgetting the base case (results in infinite calls until crash).
- Making the recursive step too large (doesn't move toward base case).

## 🏆 Key Takeaways
- Recursion is elegant for tree-like structures or math sequences.
- Every recursive problem can also be solved with a loop (iteration).
""",
        "questions": [
            {"text": "What is the condition that stops a recursive function called?", "options": [
                {"text": "Base Case", "correct": True}, {"text": "Stop Case", "correct": False},
                {"text": "Exit Point", "correct": False}, {"text": "Break Point", "correct": False}]},
            {"text": "What happens if a recursive function has no base case?", "options": [
                {"text": "RecursionError (Maximum depth exceeded)", "correct": True},
                {"text": "It returns None", "correct": False},
                {"text": "It loops forever without crashing", "correct": False},
                {"text": "It runs the command line", "correct": False}]},
        ],
        "challenge": {
            "title": "Recursive Sum",
            "description": "Define a recursive `rec_sum(n)` that returns the sum of 1 to N. Example: `rec_sum(5)` -> 15. Print `rec_sum(5)`.",
            "initial_code": "# Define recursive sum\n",
            "solution_code": "def rec_sum(n):\n    if n <= 1: return n\n    return n + rec_sum(n - 1)\nprint(rec_sum(5))\n",
            "test_cases": [{"input": "", "expected": "15"}],
        },
    },

    "les-functions-9-intermediate": {
        "title": "Recursion Depth & Tail Recursion",
        "content": """# Recursion Depth & Tail Recursion

## 🎯 Learning Objectives
- Check and change the recursion limit with `sys`
- Understand why Python does NOT optimize tail-calls
- Compare memory usage of Recursion vs Loops

## 📚 Concept Overview
Python has a safety limit (usually 1000) to prevent a system crash from deep recursion.

```python
import sys
print(sys.getrecursionlimit()) # 1000
```

### Tail Recursion
In some languages, a function call at the very end of another function uses no extra memory. **Python does not do this.** Every call adds to the stack.

## 🏆 Key Takeaways
- For huge iterations, use a loop to avoid stack overflow.
- Recursion uses O(N) memory due to the call stack.
""",
        "questions": [
            {"text": "Which module allows you to change the recursion limit?", "options": [
                {"text": "sys", "correct": True}, {"text": "math", "correct": False},
                {"text": "os", "correct": False}, {"text": "recursion", "correct": False}]},
        ],
        "challenge": {
            "title": "Safe Fib",
            "description": "Calculate the Nth Fibonacci number recursively. N = 6, Result = 8. (0, 1, 1, 2, 3, 5, 8...)",
            "initial_code": "# Fibonacci recursion\n",
            "solution_code": "def fib(n):\n    if n <= 1: return n\n    return fib(n-1) + fib(n-2)\nprint(fib(6))\n",
            "test_cases": [{"input": "", "expected": "8"}],
        },
    },

    "les-functions-9-pro": {
        "title": "Memoization (Optimizing Recursion)",
        "content": """# Memoization (Optimizing Recursion)

## 🎯 Learning Objectives
- Use `functools.lru_cache` to speed up recursive functions
- Understand the space-time tradeoff
- Visualize the "Call Tree" of recursive operations

## 📚 Concept Overview
Recursion can be slow if it solves the same sub-problem twice (like naive Fibonacci).

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    # ... logic
```

This "remembers" the result of every call, turning an O(2^N) problem into O(N).

## 🏆 Key Takeaways
- Memoization is the standard way to fix slow recursion.
""",
        "questions": [
            {"text": "Which decorator is used for built-in memoization in Python?", "options": [
                {"text": "@lru_cache", "correct": True}, {"text": "@memoize", "correct": False},
                {"text": "@cache_all", "correct": False}, {"text": "@store", "correct": False}]},
        ],
        "challenge": {
            "title": "Fast Recursive Sum",
            "description": "Add `@lru_cache` from `functools` to a recursive function that calculates `n + sum(n-1)`. Print the result for 10.",
            "initial_code": "from functools import lru_cache\n# Apply lru_cache\n",
            "solution_code": "from functools import lru_cache\n@lru_cache(None)\ndef s(n):\n    if n == 0: return 0\n    return n + s(n-1)\nprint(s(10))\n",
            "test_cases": [{"input": "", "expected": "55"}],
        },
    },

    # ── Lesson 10: Mini Project ──────────────────────────────────────────────
    "les-functions-10-beginner": {
        "title": "Project: Basic Calculator",
        "content": """# Project: Basic Calculator

## 🎯 Goal
Build a calculator by splitting logic into separate functions.

## 📝 Features
- `add(a, b)`
- `subtract(a, b)`
- `multiply(a, b)`
- `divide(a, b)`

```python
def add(a, b): return a + b
# ... etc
```
""",
        "questions": [],
        "challenge": {
            "title": "Function Dispatcher",
            "description": "Define 4 math functions. Read: 'op num1 num2'. Map 'add' to add(), 'mul' to multiply(), etc. Print result.",
            "initial_code": "# Split into functions\n",
            "solution_code": "def add(a, b): return a + b\ndef mul(a, b): return a * b\nline = input().split()\nop, n1, n2 = line[0], int(line[1]), int(line[2])\nif op == 'add': print(add(n1, n2))\nelif op == 'mul': print(mul(n1, n2))\n",
            "test_cases": [{"input": "add 10 20", "expected": "30"}, {"input": "mul 5 4", "expected": "20"}],
        },
    },

    "les-functions-10-intermediate": {
        "title": "Project: Data Processor Plugin",
        "content": """# Project: Data Processor Plugin

## 🎯 Goal
Build a function that cleans a list of strings but allows the user to provide a custom cleaning function.

## 📝 Features
- Higher-order function `clean_data(items, plugin)`
- Default plugin: lowercase
- Custom plugin: strip whitespace
""",
        "questions": [],
        "challenge": {
            "title": "Plugin Processor",
            "description": "Define `process(items, func)`. Pass a list of strings and a lambda that converts string to uppercase. Return processed list.",
            "initial_code": "# Use higher-order pattern\n",
            "solution_code": "def process(items, func):\n    return [func(i) for i in items]\nwords = input().split()\nprint(process(words, lambda x: x.upper()))\n",
            "test_cases": [{"input": "apple banana", "expected": "['APPLE', 'BANANA']"}],
        },
    },

    "les-functions-10-pro": {
        "title": "Project: Recursive Directory Scanner",
        "content": """# Project: Recursive Directory Scanner

## 🎯 Goal
Simulate scanning a file system using recursion.

## 📝 Concept
- A directory contains files and other directories.
- To count all files, you must scan inside every sub-folder.
""",
        "questions": [],
        "challenge": {
            "title": "File Counter",
            "description": "A 'Folder' is a list like `['file1.txt', ['file2.txt', 'file3.txt'], 'file4.txt']`. Write a recursive function that counts all strings (files) regardless of nesting depth.",
            "initial_code": "# Recursive count\n",
            "solution_code": "def count_files(lst):\n    count = 0\n    for item in lst:\n        if isinstance(item, list): count += count_files(item)\n        else: count += 1\n    return count\n# Input provided as list\nprint(count_files(['a', ['b', 'c'], 'd']))\n",
            "test_cases": [{"input": "", "expected": "4"}],
        },
    },
}

class Command(BaseCommand):
    help = "Hydrate Module 4 Functions Lessons 6-10"

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
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Hydrated {count} lessons in Module 4 (6-10)"))
