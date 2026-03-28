"""python manage.py hydrate_module4 -- Module 4 Functions Lessons 1-5"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Lesson, Quiz, Question, Challenge

LESSONS = {
    # ── Lesson 1: Defining Functions ─────────────────────────────────────────
    "les-functions-1-beginner": {
        "title": "Defining & Calling Functions",
        "content": """# Defining & Calling Functions

## 🎯 Learning Objectives
- Understand why we use functions (DRY principle)
- Create functions using the `def` keyword
- Call functions with proper syntax

## 📚 Concept Overview
A **function** is a reusable block of code that performs a specific task. They help you avoid repeating yourself (DRY: Don't Repeat Yourself).

```python
def greet():
    print("Hello, World!")

# Calling the function
greet()
```

### Docstrings
You should document what your function does using triple-quoted strings at the start.
```python
def greet():
    \"\"\"Print a greeting message.\"\"\"
    print("Hello!")
```

## 🏆 Key Takeaways
- Use `def` to define a function.
- A function does not run until you **call** it by its name followed by `()`.
- Functions should have a single, clear purpose.
""",
        "questions": [
            {"text": "Which keyword is used to define a function in Python?", "options": [
                {"text": "def", "correct": True}, {"text": "function", "correct": False},
                {"text": "define", "correct": False}, {"text": "func", "correct": False}]},
            {"text": "What are the triple-quoted strings at the beginning of a function called?", "options": [
                {"text": "Docstrings", "correct": True}, {"text": "Comments", "correct": False},
                {"text": "Helpstrings", "correct": False}, {"text": "Meta-text", "correct": False}]},
            {"text": "How do you execute a function named 'start'?", "options": [
                {"text": "start()", "correct": True}, {"text": "call start", "correct": False},
                {"text": "run start", "correct": False}, {"text": "start{}", "correct": False}]},
        ],
        "challenge": {
            "title": "Greeting Bot",
            "description": "Define a function named `say_hello` that prints 'Hello!'. Then call that function.",
            "initial_code": "# Define and call say_hello\n",
            "solution_code": "def say_hello():\n    print('Hello!')\nsay_hello()\n",
            "test_cases": [{"input": "", "expected": "Hello!"}],
        },
    },

    "les-functions-1-intermediate": {
        "title": "Function Design & Docstring Formats",
        "content": """# Function Design & Docstring Formats

## 🎯 Learning Objectives
- Use standard docstring formats (Google, NumPy style)
- Understand the difference between printing and returning (preview)
- Apply descriptive naming conventions (PEP 8)

## 📚 Concept Overview
### Naming Functions
Functions should be named using **snake_case** and should be verbs that describe the action.
Good: `calculate_total`, `fetch_user_data`
Bad: `calc`, `get_stuff`, `func1`

### Docstring Standards (Google Style)
```python
def add_nums(a, b):
    \"\"\"Adds two numbers together.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The sum of a and b.
    \"\"\"
    return a + b
```

## 🏆 Key Takeaways
- Naming matters! Make your functions descriptive.
- Docstrings are accessible via `help(function_name)`.
""",
        "questions": [
            {"text": "According to PEP 8, what is the naming convention for functions?", "options": [
                {"text": "snake_case", "correct": True}, {"text": "camelCase", "correct": False},
                {"text": "PascalCase", "correct": False}, {"text": "UPPERCASE", "correct": False}]},
        ],
        "challenge": {
            "title": "Helpful Multiplier",
            "description": "Define a function named `multiply_two` that takes no inputs and prints 'Multiplies two numbers'. Include a docstring 'Product logic'. Call the function.",
            "initial_code": "# Define multiply_two with a docstring\n",
            "solution_code": "def multiply_two():\n    '''Product logic'''\n    print('Multiplies two numbers')\nmultiply_two()\n",
            "test_cases": [{"input": "", "expected": "Multiplies two numbers"}],
        },
    },

    "les-functions-1-pro": {
        "title": "Metadata & __doc__ Internal Attribute",
        "content": """# Metadata & __doc__ Internal Attribute

## 🎯 Learning Objectives
- Access function metadata via `__doc__` and `__name__`
- Understand that functions are first-class objects
- Introduction to function introspection

## 📚 Concept Overview
In Python, functions are objects just like everything else. They have attributes.

```python
def my_func():
    \"\"\"Top secret info.\"\"\"
    pass

print(my_func.__name__) # 'my_func'
print(my_func.__doc__)  # 'Top secret info.'
```

### Introspection
You can pass functions around as arguments, store them in lists, and inspect their properties.

## 🏆 Key Takeaways
- Functions are objects that can be manipulated in code.
- `__doc__` stores the docstring programmatically.
""",
        "questions": [
            {"text": "Which attribute stores the docstring of a function object?", "options": [
                {"text": "__doc__", "correct": True}, {"text": ".doc", "correct": False},
                {"text": "__text__", "correct": False}, {"text": "__meta__", "correct": False}]},
        ],
        "challenge": {
            "title": "Name Inspector",
            "description": "Define a function `test_func`. Print its `__name__` attribute.",
            "initial_code": "# Print __name__ of test_func\n",
            "solution_code": "def test_func():\n    pass\nprint(test_func.__name__)\n",
            "test_cases": [{"input": "", "expected": "test_func"}],
        },
    },

    # ── Lesson 2: Arguments & Parameters ─────────────────────────────────────
    "les-functions-2-beginner": {
        "title": "Arguments & Parameters",
        "content": """# Arguments & Parameters

## 🎯 Learning Objectives
- Differentiate between a parameter and an argument
- Pass multiple arguments to a function
- Understand positional arguments

## 📚 Concept Overview
- **Parameters**: The labels in the definition (`def func(name):`)
- **Arguments**: The actual values you pass into the function (`func("Alice")`)

```python
def greet_user(name, city):
    print(f"Hello {name} from {city}")

greet_user("Alice", "London") # "Alice" and "London" are arguments
```

### Positional Arguments
By default, Python matches arguments to parameters based on their **position**.

## ⚠️ Common Pitfalls
- Passing the wrong number of arguments (raises `TypeError`).
- Passing arguments in the wrong order.

## 🏆 Key Takeaways
- Arguments are passed into functions to make them dynamic.
- The order of arguments must match the order of parameters.
""",
        "questions": [
            {"text": "What is the name for the variables listed in the function definition?", "options": [
                {"text": "Parameters", "correct": True}, {"text": "Arguments", "correct": False},
                {"text": "Outputs", "correct": False}, {"text": "Keywords", "correct": False}]},
            {"text": "In `def add(a, b):`, the values of `a` and `b` are matched by what?", "options": [
                {"text": "Position", "correct": True}, {"text": "Alphabetical order", "correct": False},
                {"text": "Size", "correct": False}, {"text": "Random", "correct": False}]},
        ],
        "challenge": {
            "title": "Simple Adder",
            "description": "Define a function `add_two` that takes two parameters `a` and `b`. Print the result of `a + b`. Call the function with 10 and 20.",
            "initial_code": "# Define add_two and call it\n",
            "solution_code": "def add_two(a, b):\n    print(a + b)\nadd_two(10, 20)\n",
            "test_cases": [{"input": "", "expected": "30"}],
        },
    },

    "les-functions-2-intermediate": {
        "title": "Keyword Arguments (Kwargs)",
        "content": """# Keyword Arguments (Kwargs)

## 🎯 Learning Objectives
- Pass arguments by name (keyword arguments)
- Mix positional and keyword arguments
- Improve code readability for functions with many parameters

## 📚 Concept Overview
Keyword arguments allow you to pass values specifically by the parameter name, making the order irrelevant.

```python
def describe_pet(animal_type, pet_name):
    print(f"I have a {animal_type} named {pet_name}.")

# Positional
describe_pet("hamster", "harry")

# Keyword (much clearer!)
describe_pet(pet_name="harry", animal_type="hamster")
```

### Mixing Types
You can mix them, but **positional arguments must come first**.
`func(10, b=20)` is OK.
`func(a=10, 20)` is an ERROR.

## 🏆 Key Takeaways
- Keyword arguments make code more explicit and harder to break if parameters are reordered.
- Always put positional arguments before keyword arguments.
""",
        "questions": [
            {"text": "Can you put a positional argument after a keyword argument in a function call?", "options": [
                {"text": "No", "correct": True}, {"text": "Yes", "correct": False},
                {"text": "Only for strings", "correct": False}, {"text": "Only in version 3.12", "correct": False}]},
        ],
        "challenge": {
            "title": "Explicit Greeting",
            "description": "Define `greet(name, message)`. Call it using keyword arguments so name is 'Bob' and message is 'Good Morning'. Output: 'Good Morning, Bob'.",
            "initial_code": "# Call with keyword args\n",
            "solution_code": "def greet(name, message):\n    print(f'{message}, {name}')\ngreet(message='Good Morning', name='Bob')\n",
            "test_cases": [{"input": "", "expected": "Good Morning, Bob"}],
        },
    },

    "les-functions-2-pro": {
        "title": "Keyword-Only & Positional-Only parameters",
        "content": """# Keyword-Only & Positional-Only Parameters

## 🎯 Learning Objectives
- Use the `/` and `*` symbols in function definitions
- Force callers to use specific argument styles
- Protect your API from breaking changes

## 📚 Concept Overview
### Keyword-Only (`*`)
Everything after the `*` must be passed as a keyword.
```python
def process_data(data, *, version=1):
    pass

process_data([1,2], version=2) # OK
process_data([1,2], 2)         # ERROR
```

### Positional-Only (`/`)
Everything before the `/` must be passed by position.
```python
def power(base, exponent, /):
    return base ** exponent
```

## 🏆 Key Takeaways
- Use `/` and `*` to strictly control how your functions are called.
- This is very common in library development to ensure clean APIs.
""",
        "questions": [
            {"text": "What does the `*` symbol represent in `def func(a, *, b):`?", "options": [
                {"text": "Following arguments must be keywords", "correct": True}, {"text": "Following arguments must be positional", "correct": False},
                {"text": "Arguments are optional", "correct": False}, {"text": "Multiplication", "correct": False}]},
        ],
        "challenge": {
            "title": "Keyword Enforcer",
            "description": "Define a function `log(msg, *, level='INFO')` that prints `[level] msg`. Call it with 'System ready' for the msg and leave the default level.",
            "initial_code": "# Define and call\n",
            "solution_code": "def log(msg, *, level='INFO'):\n    print(f'[{level}] {msg}')\nlog('System ready')\n",
            "test_cases": [{"input": "", "expected": "[INFO] System ready"}],
        },
    },

    # ── Lesson 3: Default Values & Type Hinting ──────────────────────────────
    "les-functions-3-beginner": {
        "title": "Default Argument Values",
        "content": """# Default Argument Values

## 🎯 Learning Objectives
- Provide default values for parameters
- Make functions more flexible by making arguments optional
- Order parameters with defaults correctly

## 📚 Concept Overview
You can make a function handle common cases automatically by providing a default value.

```python
def greet(name="User"):
    print(f"Hello, {name}")

greet()        # Hello, User
greet("Alice") # Hello, Alice
```

### Ordering
Parameters **without** defaults must always come before those **with** defaults.

## ⚠️ Common Pitfalls
- **Mutable Defaults**: Never use a mutable object (like a list) as a default value. It stays in memory between calls!
- WRONG: `def add_item(i, lst=[])` — The list will keep growing every time you call it!
- RIGHT: `def add_item(i, lst=None)` then check `if lst is None: lst = []`.

## 🏆 Key Takeaways
- Defaults make your code more robust and easier to use.
- Be extremely careful with empty lists or dicts as defaults.
""",
        "questions": [
            {"text": "What is the danger of using `[]` as a default argument?", "options": [
                {"text": "The same list object is shared across all function calls", "correct": True}, {"text": "It raises a SyntaxError", "correct": False},
                {"text": "It is slow", "correct": False}, {"text": "It is not allowed in Python 3", "correct": False}]},
            {"text": "In a definition, parameters with defaults must be placed:", "options": [
                {"text": "After non-default parameters", "correct": True}, {"text": "Before non-default parameters", "correct": False},
                {"text": "Anywhere", "correct": False}, {"text": "In a separate def block", "correct": False}]},
        ],
        "challenge": {
            "title": "Flexible Greeting",
            "description": "Define `power(base, exponent=2)`. Print result. Call with `5` (to get 25) and `2, 3` (to get 8).",
            "initial_code": "# Define power with a default\n",
            "solution_code": "def power(base, exponent=2):\n    print(base ** exponent)\npower(5)\npower(2, 3)\n",
            "test_cases": [{"input": "", "expected": "25\n8"}],
        },
    },

    "les-functions-3-intermediate": {
        "title": "Type Hinting in Functions",
        "content": """# Type Hinting in Functions

## 🎯 Learning Objectives
- Specify expected types for parameters using annotations
- Specify the expected return type
- Understand that Python remains dynamically typed (hints are not enforced)

## 📚 Concept Overview
Type hints make your code much easier for other humans and IDEs to understand.

```python
def add(a: int, b: int) -> int:
    return a + b
```

### Key types from `typing`
```python
from typing import List, Optional

def greets(names: List[str], count: Optional[int] = None):
    pass
```

## 🏆 Key Takeaways
- Type hints improve code quality and autocompletion.
- They are ignored by the Python runner but checked by tools like `mypy`.
""",
        "questions": [
            {"text": "Does Python enforce type hints at runtime?", "options": [
                {"text": "No", "correct": True}, {"text": "Yes", "correct": False},
                {"text": "Only in strict mode", "correct": False}, {"text": "Only for integers", "correct": False}]},
        ],
        "challenge": {
            "title": "Hinted Adder",
            "description": "Define a function `multiply(a: int, b: int) -> None` that prints the product. Call it with 5 and 6.",
            "initial_code": "# Use type hints\n",
            "solution_code": "def multiply(a: int, b: int) -> None:\n    print(a * b)\nmultiply(5, 6)\n",
            "test_cases": [{"input": "", "expected": "30"}],
        },
    },

    "les-functions-3-pro": {
        "title": "Annotation Metadata & Inspection",
        "content": """# Annotation Metadata & Inspection

## 🎯 Learning Objectives
- Inspect function annotations at runtime via `__annotations__`
- Understand how modern frameworks (like FastAPI) use hints for data validation
- Explore Advanced types like `Callable` and `Union`

## 📚 Concept Overview
Annotations are stored in a dictionary and can be read by other parts of your program.

```python
def test(a: int): pass
print(test.__annotations__) # {'a': <class 'int'>}
```

This is how powerful tools can automatically generate APIs or documentation from your code.

## 🏆 Key Takeaways
- Annotations are more than just comments; they are accessible metadata.
""",
        "questions": [
            {"text": "Where are function annotations stored in a function object?", "options": [
                {"text": "__annotations__", "correct": True}, {"text": "__hints__", "correct": False},
                {"text": "__metadata__", "correct": False}, {"text": ".types", "correct": False}]},
        ],
        "challenge": {
            "title": "Hint Inspector",
            "description": "Define `example(x: str)`. Print the `__annotations__` dictionary.",
            "initial_code": "# Print annotations\n",
            "solution_code": "def example(x: str):\n    pass\nprint(example.__annotations__)\n",
            "test_cases": [{"input": "", "expected": "{'x': <class 'str'>}"}],
        },
    },

    # ── Lesson 4: Return Values ──────────────────────────────────────────────
    "les-functions-4-beginner": {
        "title": "The Return Statement",
        "content": """# The Return Statement

## 🎯 Learning Objectives
- Send data back from a function using `return`
- Understand the difference between `print()` and `return`
- Capture return values in variables

## 📚 Concept Overview
While `print()` displays text to the screen, `return` lets the function output a value that can be reused later in the program.

```python
def add(a, b):
    return a + b

result = add(5, 10) # result is now 15
print(result * 2)   # 30
```

### Exiting early
A function stops running as soon as it hits a `return`.

## 🏆 Key Takeaways
- Use `return` when you need to use the function's result for another operation.
- Code after a executed `return` statement is never reached.
- If no `return` is specified, a function returns `None`.
""",
        "questions": [
            {"text": "What happens to the code lines in a function after a `return` is executed?", "options": [
                {"text": "They are never executed", "correct": True}, {"text": "They are executed normally", "correct": False},
                {"text": "They cause an error", "correct": False}, {"text": "They are printed", "correct": False}]},
            {"text": "What value is returned by default if there is no `return` statement?", "options": [
                {"text": "None", "correct": True}, {"text": "0", "correct": False},
                {"text": "False", "correct": False}, {"text": "Empty String", "correct": False}]},
        ],
        "challenge": {
            "title": "Calculated Result",
            "description": "Define `square(n)`. It should RETURN the square of n. Call it with 4 and print the result multiplied by 10.",
            "initial_code": "# Use return\n",
            "solution_code": "def square(n):\n    return n * n\nprint(square(4) * 10)\n",
            "test_cases": [{"input": "", "expected": "160"}],
        },
    },

    "les-functions-4-intermediate": {
        "title": "Returning Multiple Values",
        "content": """# Returning Multiple Values

## 🎯 Learning Objectives
- Return more than one value using Tuples
- Unpack multiple return values directly into variables
- Grasp how Python treats commas as implicit tuple creation

## 📚 Concept Overview
You can return multiple items by separating them with commas. Python packs them into a **tuple**.

```python
def get_user():
    return "Alice", 25, "Designer"

name, age, job = get_user() # Unpacking
print(f"{name} is a {job}")
```

## 🏆 Key Takeaways
- Functions can "output" multiple things at once.
- Unpacking makes this extremely clean and readable.
""",
        "questions": [
            {"text": "What type of object is returned when you use `return a, b`?", "options": [
                {"text": "Tuple", "correct": True}, {"text": "List", "correct": False},
                {"text": "Dictionary", "correct": False}, {"text": "String", "correct": False}]},
        ],
        "challenge": {
            "title": "MinMax Return",
            "description": "Define `min_max(a, b)`. Return both the smaller and then the larger value. Call with 50, 10 and print the results.",
            "initial_code": "# Return two values\n",
            "solution_code": "def min_max(a, b):\n    if a < b: return a, b\n    else: return b, a\nlow, high = min_max(50, 10)\nprint(low, high)\n",
            "test_cases": [{"input": "", "expected": "10 50"}],
        },
    },

    "les-functions-4-pro": {
        "title": "Return Typing & Generator Basics",
        "content": """# Return Typing & Generator Basics

## 🎯 Learning Objectives
- Use `Union` and `Any` for flexible returns
- Introduction to `yield` (Generators)
- Comparison of resource usage between Return and Yield

## 📚 Concept Overview
### yield
If you use `yield` instead of `return`, your function becomes a **Generator**. It returns a sequence of values over time instead of all at once.

```python
def count_down(n):
    while n > 0:
        yield n
        n -= 1
```

## 🏆 Key Takeaways
- `return` sends back everything and ends the function.
- `yield` pauses the function and keeps its state for the next call.
""",
        "questions": [
            {"text": "Which keyword turns a function into a generator?", "options": [
                {"text": "yield", "correct": True}, {"text": "return", "correct": False},
                {"text": "produce", "correct": False}, {"text": "emit", "correct": False}]},
        ],
        "challenge": {
            "title": "Simple Generator",
            "description": "Define a generator `gen()` that yields 1 then 2. Print both values using a loop or manual calls.",
            "initial_code": "# Use yield\n",
            "solution_code": "def gen():\n    yield 1\n    yield 2\nfor val in gen():\n    print(val)\n",
            "test_cases": [{"input": "", "expected": "1\n2"}],
        },
    },

    # ── Lesson 5: Variable Scope ──────────────────────────────────────────────
    "les-functions-5-beginner": {
        "title": "Local vs Global Scope",
        "content": """# Local vs Global Scope

## 🎯 Learning Objectives
- Understand the "Visibility" of variables
- Distinguish between variables inside and outside functions
- Grasp the lifecycle of a local variable

## 📚 Concept Overview
- **Global Scope**: Variables defined outside functions. Visible everywhere.
- **Local Scope**: Variables defined inside a function. Only visible there.

```python
x = "Global"

def test():
    y = "Local"
    print(x) # OK
    print(y) # OK

test()
print(y) # ERROR: y doesn't exist out here!
```

## ⚠️ Common Pitfalls
- Assuming a function can modify a global variable directly (it creates a new local one instead).
- Naming local and global variables the same (Shadowing).

## 🏆 Key Takeaways
- Local variables are destroyed once the function finishes.
- Functions can "read" global variables, but not "write" to them by default.
""",
        "questions": [
            {"text": "A variable defined inside a function is known as:", "options": [
                {"text": "Local variable", "correct": True}, {"text": "Global variable", "correct": False},
                {"text": "Public variable", "correct": False}, {"text": "Static variable", "correct": False}]},
            {"text": "Can you access a local variable outside its function?", "options": [
                {"text": "No", "correct": True}, {"text": "Yes", "correct": False},
                {"text": "Only if using return", "correct": False}, {"text": "Only for numbers", "correct": False}]},
        ],
        "challenge": {
            "title": "Scope Trap",
            "description": "Define a global `msg = 'Global'`. Define a function that creates a local `msg = 'Local'`. Print the local one inside and the global one outside.",
            "initial_code": "# Demonstrate shadowing\n",
            "solution_code": "msg = 'Global'\ndef show():\n    msg = 'Local'\n    print(msg)\nshow()\nprint(msg)\n",
            "test_cases": [{"input": "", "expected": "Local\nGlobal"}],
        },
    },

    "les-functions-5-intermediate": {
        "title": "The Global & Nonlocal Keywords",
        "content": """# The Global & Nonlocal Keywords

## 🎯 Learning Objectives
- Use the `global` keyword to modify global variables
- Use the `nonlocal` keyword for nested functions
- Understand the risks of using global state

## 📚 Concept Overview
If you **must** change a global variable inside a function, use `global`.
```python
x = 10
def change():
    global x
    x = 20
```

### nonlocal
Used when you have a function inside another function and want to modify the parent's variable.

## 🏆 Key Takeaways
- Avoid `global` if possible; it makes code unpredictable and hard to test.
- Prefer passing values as arguments and returning changes.
""",
        "questions": [
            {"text": "Which keyword allows you to modify a variable in the nearest outer (non-global) scope?", "options": [
                {"text": "nonlocal", "correct": True}, {"text": "global", "correct": False},
                {"text": "parent", "correct": False}, {"text": "outer", "correct": False}]},
        ],
        "challenge": {
            "title": "Global Counter",
            "description": "Use a global `count = 0`. Create a function `inc()` that uses the `global` keyword to increase it by 1. Call it 3 times and print the final count.",
            "initial_code": "count = 0\n# Use global to increment\n",
            "solution_code": "count = 0\ndef inc():\n    global count\n    count += 1\ninc()\ninc()\ninc()\nprint(count)\n",
            "test_cases": [{"input": "", "expected": "3"}],
        },
    },

    "les-functions-5-pro": {
        "title": "The LEGB Rule & Closure Basics",
        "content": """# The LEGB Rule & Closure Basics

## 🎯 Learning Objectives
- Master the LEGB Lookup order (Local, Enclosing, Global, Built-in)
- Understand "Closures" — functions that remember their environment
- Predict variable resolution in complex scenarios

## 📚 Concept Overview
Python looks for variables in this order:
1. **L**ocal: Inside the function.
2. **E**nclosing: In nested functions.
3. **G**lobal: At the top level of the file.
4. **B**uilt-in: Python's internal names (like `len`).

### Closures
A closure is a function that "closes over" variables from its outer scope even after the outer function has finished.

## 🏆 Key Takeaways
- LEGB is how Python finds every single name in your code.
- Closures are powerful for creating function factories.
""",
        "questions": [
            {"text": "What does LEGB stand for?", "options": [
                {"text": "Local, Enclosing, Global, Built-in", "correct": True}, {"text": "Loop, Error, Global, Boolean", "correct": False},
                {"text": "List, Entry, Get, Binary", "correct": False}, {"text": "Last, Each, Group, Batch", "correct": False}]},
        ],
        "challenge": {
            "title": "Closure Power",
            "description": "Create a function `make_adder(n)` that returns a nested function. The nested function should take `x` and return `x + n`. Call `make_adder(10)` and then use the resulting function to add 5.",
            "initial_code": "# Closure pattern\n",
            "solution_code": "def make_adder(n):\n    def adder(x):\n        return x + n\n    return adder\nadd10 = make_adder(10)\nprint(add10(5))\n",
            "test_cases": [{"input": "", "expected": "15"}],
        },
    },
}

class Command(BaseCommand):
    help = "Hydrate Module 4 Functions Lessons 1-5"

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
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Hydrated {count} lessons in Module 4 (1-5)"))
