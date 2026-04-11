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
    Generates high-quality, structured, and difficulty-appropriate markdown content.
    """
    title = spec.title.replace(f" ({spec.difficulty})", "")
    level = spec.difficulty
    topic = spec.topic

    # Content generation logic based on topic and difficulty
    content_blocks = []

    # 1. Definition / Explanation
    explanations = {
        "input_output": {
            "Beginner": "Input and Output (I/O) are the most basic ways your program communicates. Output is how the computer 'talks' to you, while Input is how you 'talk' to the computer.",
            "Intermediate": "Python's I/O involves the `print()` and `input()` functions. `print()` formats and displays data to the standard output, while `input()` captures user data as strings from the standard input.",
            "Pro": "Advanced I/O in Python goes beyond `print()`. It involves formatted string literals (f-strings), stream handling, and understanding how `sys.stdin` and `sys.stdout` work under the hood for efficient data processing."
        },
        "variables": {
            "Beginner": "Think of a variable as a labeled box where you can store information. You give the box a name, like `score`, and put a value inside, like `10`.",
            "Intermediate": "Variables in Python are symbolic names that serve as references to objects. Python uses dynamic typing, meaning you don't need to declare the type of data a variable will hold.",
            "Pro": "Python variables are references to objects in memory. Understanding variable assignment involves understanding object identity (`id()`), mutability, and how Python's memory management handles reference counting."
        },
        "types": {
            "Beginner": "Data types tell Python what kind of information you are working with. Common types include whole numbers (integers), decimal numbers (floats), and text (strings).",
            "Intermediate": "Python's built-in data types include numeric types (`int`, `float`, `complex`), sequence types (`str`, `list`, `tuple`), and mapping types (`dict`). Each type has specific properties like mutability.",
            "Pro": "Advanced data typing involves understanding the underlying implementation of Python objects, type hinting for static analysis, and using the `typing` module for complex structures like `Union`, `Optional`, and `Callable`."
        },
        "operators": {
            "Beginner": "Operators are special symbols used to perform calculations. You use `+` for addition, `-` for subtraction, and `*` for multiplication, just like in math class.",
            "Intermediate": "Python supports various operators: arithmetic (`+`, `//`, `%`), comparison (`==`, `!=`, `>`), and logical (`and`, `or`, `not`). Understanding operator precedence is key to writing correct expressions.",
            "Pro": "Pro-level operators include bitwise operators (`&`, `|`, `^`), membership operators (`in`), and identity operators (`is`). We also look at operator overloading in classes using dunder methods like `__add__`."
        },
        "strings": {
            "Beginner": "Strings are used for text. In Python, you create a string by putting text inside single quotes `'hi'` or double quotes `\"hi\"`.",
            "Intermediate": "Strings are immutable sequences of Unicode characters. You can manipulate them using methods like `.upper()`, `.split()`, and `.strip()`, or by using slicing `text[0:5]`.",
            "Pro": "Advanced string handling involves regular expressions (`re` module), efficient concatenation using `.join()`, and understanding the difference between byte strings and Unicode strings for file encoding."
        },
        "booleans": {
            "Beginner": "Booleans represent truth values: `True` or `False`. They are the foundation of all computer logic and decision making.",
            "Intermediate": "Boolean logic in Python uses `True` and `False` (which are actually integers 1 and 0). We use comparison operators like `==`, `!=`, `<`, and `>` to generate boolean values.",
            "Pro": "Advanced boolean logic involves short-circuit evaluation in `and`/`or` expressions and understanding 'truthiness' (which non-boolean objects evaluate to True or False)."
        },
        "if_else": {
            "Beginner": "Conditional statements allow your program to make decisions. An `if` statement runs code only if a certain condition is true.",
            "Intermediate": "The `if-else` structure handles two paths: one for when a condition is true, and another for when it's false. This is essential for branching logic.",
            "Pro": "Pro-level conditionals involve nested `if` statements, combining multiple conditions with logical operators, and using ternary operators for concise code."
        },
        "elif": {
            "Beginner": "The `elif` keyword is short for 'else if'. It lets you check multiple conditions in a row until one of them is true.",
            "Intermediate": "Chaining `if-elif-else` allows for complex decision trees. Python executes the block of the first condition that evaluates to True and skips the rest.",
            "Pro": "Advanced multi-way branching involves understanding the performance of long `elif` chains versus dictionary dispatching or the `match-case` statement (Python 3.10+)."
        },
        "logic_ops": {
            "Beginner": "Logical operators (`and`, `or`, `not`) let you combine multiple conditions together to make more complex decisions.",
            "Intermediate": "We explore the truth tables for `and`, `or`, and `not`. Understanding how to combine these operators correctly is vital for complex control flow.",
            "Pro": "Advanced usage includes short-circuiting behavior (e.g., `a or b` doesn't evaluate `b` if `a` is true) and using logical operators for assignment defaults."
        },
        "nested_if": {
            "Beginner": "A nested `if` is simply an `if` statement inside another `if`. It's like having a second question that only gets asked if the first answer was 'Yes'.",
            "Intermediate": "Nested conditionals allow for granular decision making. However, too much nesting can make code hard to read, leading to the need for refactoring.",
            "Pro": "Professional developers avoid deep nesting by using guard clauses, early returns, or boolean logic to flatten the structure for better maintainability."
        },
        "loops_for": {
            "Beginner": "A `for` loop is used to repeat a block of code a specific number of times or for every item in a collection like a list.",
            "Intermediate": "We use `for` loops with the `range()` function and explore iterating over strings and lists. We also look at the `enumerate()` function for getting indexes.",
            "Pro": "Advanced iteration involves list comprehensions, generator expressions, and using the `itertools` module for efficient looping over large datasets."
        },
        "loops_while": {
            "Beginner": "A `while` loop keeps running as long as a condition remains true. It's like saying 'Keep walking while the light is green'.",
            "Intermediate": "We explore controlled `while` loops with counters and flags. Understanding how to avoid infinite loops by correctly updating the condition is key.",
            "Pro": "Advanced `while` loops are used for event loops, network listeners, and scenarios where the number of iterations isn't known in advance."
        },
        "functions_def": {
            "Beginner": "Functions are reusable blocks of code that perform a specific task. They help you avoid repeating yourself and make your code organized.",
            "Intermediate": "Defining functions involves using the `def` keyword, naming the function, and understanding how to call it from other parts of your program.",
            "Pro": "Professional function design involves writing pure functions, understanding closures, and using decorators to extend function behavior without modifying the source."
        },
        "lists": {
            "Beginner": "A list is an ordered collection of items. You can store many values in a single variable using square brackets `[]`.",
            "Intermediate": "We look at list mutability and common methods like `.append()`, `.pop()`, and `.sort()`. We also explore slicing to get sub-sections of a list.",
            "Pro": "Pro-level list usage involves understanding the underlying dynamic array implementation, time complexity of operations, and using `bisect` for sorted lists."
        },
        "classes": {
            "Beginner": "Classes are blueprints for creating objects. An object is a collection of data (attributes) and behaviors (methods) that represent something real.",
            "Intermediate": "We explore the `class` keyword, the `self` parameter, and how to create instances. We also look at how attributes and methods are organized.",
            "Pro": "Advanced OOP involves inheritance, polymorphism, mixins, and understanding the MRO (Method Resolution Order) and metaclasses."
        },
        "mini_project_1": {
            "Beginner": "Build a Greeting App! Ask for a name and print a welcome message.",
            "Intermediate": "Build a smart Greeting App with input validation and professional formatting.",
            "Pro": "Build a Greeting System with user logging, randomized messages, and modular functions."
        }
    }

    # Fallback for other modules/topics to ensure no empty fields
    default_explanations = {
        "Beginner": f"In this lesson, we explore the basics of {title}. We will focus on simple concepts and how to get started quickly.",
        "Intermediate": f"This lesson provides a deeper look into {title}, covering practical implementations and common patterns used in real-world Python code.",
        "Pro": f"We dive into advanced aspects of {title}, focusing on performance, edge cases, and architectural best practices for professional developers."
    }

    explanation = explanations.get(topic, {}).get(level, default_explanations[level])

    content_blocks.append(f"# {title}")
    content_blocks.append(f"**Level**: {level}  \n**Topic**: {topic}")
    content_blocks.append(f"## 1. Explanation\n{explanation}")

    # 2 & 3. Types and Detailed Explanation
    if topic == "types":
        if level == "Beginner":
            content_blocks.append("## 2. Common Types\n- **int**: Whole numbers (5, -10)\n- **float**: Decimal numbers (3.14, 0.5)\n- **str**: Text ('Hello')")
            content_blocks.append("## 3. Details\nPython knows what type a value is based on how you write it. If it has quotes, it's a string. If it has a decimal point, it's a float.")
        elif level == "Intermediate":
            content_blocks.append("## 2. Built-in Types\n- **Numeric**: int, float, complex\n- **Sequence**: list, tuple, range\n- **Boolean**: True, False")
            content_blocks.append("## 3. Details\nSequence types like lists are 'iterable', meaning you can loop through them. Booleans are essential for making decisions in your code using logic.")
        else:
            content_blocks.append("## 2. Advanced Types\n- **Mapping**: dict\n- **Set Types**: set, frozenset\n- **Binary**: bytes, bytearray")
            content_blocks.append("## 3. Details\nDictionaries allow for O(1) average-time complexity lookups. Sets are useful for ensuring uniqueness and performing mathematical set operations like unions and intersections.")
    else:
        # Generic types block for other topics
        content_blocks.append(f"## 2. Core Concepts\nThis lesson covers the fundamental aspects of {title} including its syntax and primary usage patterns.")
        content_blocks.append(f"## 3. Deep Dive\nWhen working with {title}, it is important to understand how it interacts with other Python features to build robust applications.")

    # 4. Code Examples
    codes = {
        "input_output": {
            "Beginner": "# Beginner: Simple print and input\nprint('Hello!')\nname = input('What is your name? ')\nprint('Welcome, ' + name)",
            "Intermediate": "# Intermediate: f-strings and type conversion\nage = int(input('Enter age: '))\nprint(f'You will be {age + 1} next year!')",
            "Pro": "# Pro: Stream handling and formatting\nimport sys\nsys.stdout.write('Processing...\\n')\nfruits = ['apple', 'banana']\nprint(*(f.upper() for f in fruits), sep=' | ')"
        },
        "variables": {
            "Beginner": "# Beginner: Assignment and naming\nscore = 100\nuser_name = 'Player1'\nprint(score)",
            "Intermediate": "# Intermediate: Dynamic typing\ndata = 10\nprint(type(data))\ndata = 'Ten'\nprint(type(data))",
            "Pro": "# Pro: Object references\na = [1, 2]\nb = a\nb.append(3)\nprint(a) # [1, 2, 3] because they share the same object"
        },
        "types": {
            "Beginner": "# Beginner: Basic types\nx = 5       # int\ny = 3.14    # float\nz = 'hi'    # str\nprint(type(x))",
            "Intermediate": "# Intermediate: Collection types\nmy_list = [1, 2, 3]\nmy_tuple = (1, 2, 3)\nprint(f'List: {my_list}, Tuple: {my_tuple}')",
            "Pro": "# Pro: Type hints and complex types\nfrom typing import List, Dict\ndef process(data: List[int]) -> Dict[str, int]:\n    return {'sum': sum(data)}"
        },
        "if_else": {
            "Beginner": "# Beginner: Simple if\ntemp = 30\nif temp > 25:\n    print('It is hot!')",
            "Intermediate": "# Intermediate: if-else logic\nscore = 60\nif score >= 50:\n    print('Pass')\nelse:\n    print('Fail')",
            "Pro": "# Pro: Ternary and nested logic\nstatus = 'Adult' if age >= 18 else 'Minor'\nif age > 18:\n    if has_id: print('Access granted')"
        },
        "loops_for": {
            "Beginner": "# Beginner: Basic for loop\nfor i in range(5):\n    print(i)",
            "Intermediate": "# Intermediate: Iterating collections\ncolors = ['red', 'green', 'blue']\nfor color in colors:\n    print(f'Color: {color}')",
            "Pro": "# Pro: List comprehensions\nnums = [1, 2, 3, 4]\nsquares = [x**2 for x in nums if x % 2 == 0]\nprint(squares)"
        },
        "lists": {
            "Beginner": "# Beginner: Creating and accessing\nitems = ['pen', 'paper']\nprint(items[0])",
            "Intermediate": "# Intermediate: List methods\nitems = [1, 2]\nitems.append(3)\nitems.extend([4, 5])\nprint(items)",
            "Pro": "# Pro: Slicing and performance\nbig_list = list(range(100))\nsubset = big_list[::10] # Every 10th item\nprint(subset)"
        },
        "classes": {
            "Beginner": "# Beginner: Simple class\nclass Dog:\n    pass\nmy_dog = Dog()",
            "Intermediate": "# Intermediate: Attributes and methods\nclass Car:\n    def __init__(self, brand):\n        self.brand = brand\n    def drive(self):\n        print(f'{self.brand} is moving')",
            "Pro": "# Pro: Inheritance and super()\nclass ElectricCar(Car):\n    def __init__(self, brand, battery):\n        super().__init__(brand)\n        self.battery = battery"
        }
    }
    code = codes.get(topic, {}).get(level, "# Example code for " + title + "\nprint('Level: " + level + "')\n# Start practicing here!")
    content_blocks.append(f"## 4. Code Example\n```python\n{code}\n```")

    # 5. Real-world Use Cases
    use_cases = {
        "Beginner": "Building a simple calculator or a personal greeting script.",
        "Intermediate": "Processing user data from a web form or reading configuration files.",
        "Pro": "Developing high-performance data pipelines or building scalable backend services."
    }
    content_blocks.append(f"## 5. Real-world Use Case\n{use_cases[level]}")

    # 6. Key Takeaways
    if level == "Beginner":
        takeaways = ["Learn the basic syntax.", "Practice with simple print statements.", "Don't worry about complex logic yet."]
    elif level == "Intermediate":
        takeaways = ["Understand how different types interact.", "Use built-in methods for efficiency.", "Follow PEP 8 for clean code."]
    else:
        takeaways = ["Focus on memory and performance.", "Handle edge cases and potential errors.", "Write modular and reusable code."]
    
    content_blocks.append("## 6. Key Takeaways\n" + "\n".join([f"- {t}" for t in takeaways]))

    # 7. Knowledge Check
    content_blocks.append("## 7. Knowledge Check")
    content_blocks.append("1. What is the main goal of this topic?  \n   *Answer: To understand " + title + ".*")
    content_blocks.append("2. Is this concept used frequently in Python?  \n   *Answer: Yes, it is a core part of the language.*")

    # 8. Mini Challenge
    challenges = {
        "Beginner": "Try creating a variable and printing it to the console.",
        "Intermediate": "Write a function that takes input and returns a formatted string.",
        "Pro": "Optimize a loop or data structure for better time complexity."
    }
    content_blocks.append(f"## 8. Mini Challenge\n{challenges[level]}")

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
        "initial_code": "",  # Empty by default to encourage active learning
        "solution_code": entry["starter"], # Store the original starter as solution
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
                        "difficulty": spec.difficulty,
                    },
                )
                if ch_created:
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
