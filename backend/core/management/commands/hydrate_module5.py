"""python manage.py hydrate_module5 -- Module 5 Modules & Packages Lessons 1-5"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Lesson, Quiz, Question, Challenge

LESSONS = {
    # ── Lesson 1: What is a Module? ──────────────────────────────────────────
    "les-modules-packages-1-beginner": {
        "title": "Importing Modules",
        "content": """# Importing Modules

## 🎯 Learning Objectives
- Understand what a module is in Python
- Use the `import` keyword to access external code
- Use aliases (`as`) and `from ... import` syntax

## 📚 Concept Overview
A **module** is simply a file containing Python code (functions, classes, variables). Instead of writing everything in one giant file, you can break your code into modules.

### Basic Import
```python
import math
print(math.sqrt(16)) # 4.0
```

### Specific Import
```python
from math import pi
print(pi)
```

### Aliasing
```python
import pandas as pd # Conventional alias
```

## 🏆 Key Takeaways
- Modules promote code reuse and organization.
- `import module` brings in the whole file; `from module import name` brings only that part.
- Use aliases to save typing or avoid naming conflicts.
""",
        "questions": [
            {"text": "Which keyword is used to bring an external module into your script?", "options": [
                {"text": "import", "correct": True}, {"text": "include", "correct": False},
                {"text": "require", "correct": False}, {"text": "load", "correct": False}]},
            {"text": "How do you import the `sqrt` function specifically from the `math` module?", "options": [
                {"text": "from math import sqrt", "correct": True}, {"text": "import sqrt from math", "correct": False},
                {"text": "math.import(sqrt)", "correct": False}, {"text": "load math.sqrt", "correct": False}]},
            {"text": "What does `import math as m` do?", "options": [
                {"text": "Allows you to use 'm' instead of 'math' in your code", "correct": True},
                {"text": "Renames the math file on your disk", "correct": False},
                {"text": "Creates a copy of the math module", "correct": False},
                {"text": "Imports only the 'm' function from math", "correct": False}]},
        ],
        "challenge": {
            "title": "Square Rooter",
            "description": "Import `sqrt` from the `math` module. Read a number and print its square root rounded to 2 decimal places.",
            "initial_code": "# Use from math import sqrt\n",
            "solution_code": "from math import sqrt\nn = float(input())\nprint(round(sqrt(n), 2))\n",
            "test_cases": [{"input": "16", "expected": "4.0"}, {"input": "2", "expected": "1.41"}],
        },
    },

    "les-modules-packages-1-intermediate": {
        "title": "Module Search Path (sys.path)",
        "content": """# Module Search Path (sys.path)

## 🎯 Learning Objectives
- Understand where Python looks for modules
- Inspect the `sys.path` list
- Add custom directories to the search path

## 📚 Concept Overview
When you `import something`, Python looks in this order:
1. The **current directory** (where your script is).
2. The **Standard Library** directories.
3. Third-party packages (e.g., in your `site-packages` folder).

### sys.path
You can see this list in Python:
```python
import sys
for path in sys.path:
    print(path)
```

## ⚠️ Common Pitfalls
- **Naming conflicts**: Never name your own file `math.py` or `random.py`. If you do, `import math` will import **your** file instead of the built-in one!

## 🏆 Key Takeaways
- Python searches a prioritized list of directories for modules.
- Being aware of the search path helps debug "ModuleNotFoundError" or weird naming bugs.
""",
        "questions": [
            {"text": "Where is the first place Python looks for an imported module?", "options": [
                {"text": "The directory of the current script", "correct": True}, {"text": "The Standard Library", "correct": False},
                {"text": "The internet", "correct": False}, {"text": "The user's home folder", "correct": False}]},
            {"text": "Which module allows you to inspect the search paths?", "options": [
                {"text": "sys", "correct": True}, {"text": "os", "correct": False},
                {"text": "pathlib", "correct": False}, {"text": "importlib", "correct": False}]},
        ],
        "challenge": {
            "title": "Path Counter",
            "description": "Import `sys`. Print the number of directories currently in `sys.path`.",
            "initial_code": "# Use sys.path\n",
            "solution_code": "import sys\nprint(len(sys.path))\n",
            "test_cases": [{"input": "", "expected": "*"}], # Any number is OK since sys.path varies
        },
    },

    "les-modules-packages-1-pro": {
        "title": "Dynamic Imports & importlib",
        "content": """# Dynamic Imports & importlib

## 🎯 Learning Objectives
- Import modules dynamically using strings
- Use the `importlib` library
- Reload modules during runtime with `importlib.reload`

## 📚 Concept Overview
Sometimes you don't know the name of the module you need until the program is running.

```python
import importlib
module_name = "math"
math_mod = importlib.import_module(module_name)
print(math_mod.sqrt(25))
```

### Reloading
By default, Python only imports a module **once**. If you change the file and want to see changes without restarting Python, use:
```python
importlib.reload(my_module)
```

## 🏆 Key Takeaways
- `importlib` is the modern way to handle programmatic imports.
- It is powerful for building plugin-based systems.
""",
        "questions": [
            {"text": "Does Python re-import a module if you call `import my_mod` a second time in the same session?", "options": [
                {"text": "No, it uses the cached version in sys.modules", "correct": True},
                {"text": "Yes, it re-reads the file", "correct": False},
                {"text": "Only if the file size changed", "correct": False},
                {"text": "Only in debug mode", "correct": False}]},
        ],
        "challenge": {
            "title": "Dynamic Math",
            "description": "Use `importlib.import_module` to import the 'math' module by name. Print the value of `math.pi`.",
            "initial_code": "import importlib\n# Dynamic import\n",
            "solution_code": "import importlib\nm = importlib.import_module('math')\nprint(m.pi)\n",
            "test_cases": [{"input": "", "expected": "3.141592653589793"}],
        },
    },

    # ── Lesson 2: The Standard Library ───────────────────────────────────────
    "les-modules-packages-2-beginner": {
        "title": "The 'Batteries Included' Philosophy",
        "content": """# The 'Batteries Included' Philosophy

## 🎯 Learning Objectives
- Explore Python's Standard Library
- Use `random` for numbers and choices
- Use `math` for advanced calculations

## 📚 Concept Overview
Python comes with a huge set of built-in modules so you can start working immediately without installing anything extra.

### random
```python
import random
print(random.randint(1, 10)) # Random Int
print(random.choice(["A", "B"])) # Random element
```

### math
```python
import math
print(math.factorial(5)) # 120
```

## 🏆 Key Takeaways
- Always check the Standard Library before writing your own tools or installing 3rd party ones.
- "Batteries Included" means it has tools for everything from math to internet protocols.
""",
        "questions": [
            {"text": "Which module would you use to generate a random number?", "options": [
                {"text": "random", "correct": True}, {"text": "math", "correct": False},
                {"text": "os", "correct": False}, {"text": "rand", "correct": False}]},
            {"text": "What does 'Batteries Included' mean in Python?", "options": [
                {"text": "It comes with a large standard library for many tasks", "correct": True},
                {"text": "It requires a physical battery to run", "correct": False},
                {"text": "It is optimized for laptops", "correct": False},
                {"text": "It is open-source", "correct": False}]},
        ],
        "challenge": {
            "title": "Coin Flipper",
            "description": "Import `random`. Define a function `flip()` that returns 'Heads' or 'Tails' randomly. Call it once.",
            "initial_code": "# Use random.choice\n",
            "solution_code": "import random\ndef flip():\n    return random.choice(['Heads', 'Tails'])\nprint(flip())\n",
            "test_cases": [{"input": "", "expected": "*"}], # Random output allowed
        },
    },

    "les-modules-packages-2-intermediate": {
        "title": "Handling Dates & Times",
        "content": """# Handling Dates & Times

## 🎯 Learning Objectives
- Use the `datetime` module
- Format dates using `strftime`
- Calculate time differences using `timedelta`

## 📚 Concept Overview
```python
from datetime import datetime, timedelta

# Current time
now = datetime.now()

# Formatting (Year-Month-Day)
print(now.strftime("%Y-%m-%d"))

# Math with time
tomorrow = now + timedelta(days=1)
```

## ️🏆 Key Takeaways
- `datetime` is the standard tool for time-related logic.
- `timedelta` represents a duration, while `datetime` represents a point in time.
""",
        "questions": [
            {"text": "Which class in the `datetime` module represents a duration (difference between two times)?", "options": [
                {"text": "timedelta", "correct": True}, {"text": "timespan", "correct": False},
                {"text": "duration", "correct": False}, {"text": "timekeeper", "correct": False}]},
        ],
        "challenge": {
            "title": "Year Extractor",
            "description": "Import `datetime`. Print the current year as an integer.",
            "initial_code": "from datetime import datetime\n# Print current year\n",
            "solution_code": "from datetime import datetime\nprint(datetime.now().year)\n",
            "test_cases": [{"input": "", "expected": "*"}] # Year changes
        },
    },

    "les-modules-packages-2-pro": {
        "title": "Serializing Data (JSON & Pickle)",
        "content": """# Serializing Data (JSON & Pickle)

## 🎯 Learning Objectives
- Convert objects to strings using `json`
- Save Python objects directly using `pickle`
- Understand the security risks of `pickle`

## 📚 Concept Overview
### JSON
The universal format for web data.
```python
import json
data = {"name": "Alice"}
s = json.dumps(data) # To string
```

### Pickle
Python-specific. Can save ALMOST any Python object (even functions/classes).
**CAUTION**: Never "unpickle" data from an untrusted source, as it can execute arbitrary code!

## 🏆 Key Takeaways
- Use `json` for compatibility with other languages.
- Use `pickle` for complex Python internal objects, but keep it secure.
""",
        "questions": [
            {"text": "Which module allows you to save almost any Python object in a binary format?", "options": [
                {"text": "pickle", "correct": True}, {"text": "json", "correct": False},
                {"text": "sys", "correct": False}, {"text": "os", "correct": False}]},
            {"text": "Why should you be careful with the `pickle` module?", "options": [
                {"text": "It can run malicious code during loading", "correct": True},
                {"text": "It is very slow", "correct": False},
                {"text": "It only works with integers", "correct": False},
                {"text": "It requires a license", "correct": False}]},
        ],
        "challenge": {
            "title": "JSON Maker",
            "description": "Read a name and age. Create a dictionary and print its JSON string representation using `json.dumps()`.",
            "initial_code": "import json\n# Convert dict to JSON string\n",
            "solution_code": "import json\nname = input()\nage = int(input())\ndata = {'name': name, 'age': age}\nprint(json.dumps(data))\n",
            "test_cases": [{"input": "Alice\n25", "expected": '{"name": "Alice", "age": 25}'}],
        },
    },

    # ── Lesson 3: Creating Your Own Modules ──────────────────────────────
    "les-modules-packages-3-beginner": {
        "title": "Building Your First Module",
        "content": """# Building Your First Module

## 🎯 Learning Objectives
- Create a reusable `.py` file
- Import functions from your own file
- Organize code across multiple files

## 📚 Concept Overview
1. Create a file `utils.py`:
```python
def add(a, b): return a + b
```
2. Create your main script `main.py`:
```python
import utils
print(utils.add(5, 5))
```

## 🏆 Key Takeaways
- Any `.py` file you create is a module!
- Keep your filenames simple and unique.
""",
        "questions": [
            {"text": "If you have a file named `logic.py`, how do you use its functions in another file?", "options": [
                {"text": "import logic", "correct": True}, {"text": "load logic", "correct": False},
                {"text": "include(logic.py)", "correct": False}, {"text": "from logic.py import *", "correct": False}]},
        ],
        "challenge": {
            "title": "Module Simulator",
            "description": "Assume a module `math_plus` has a function `square(x)`. Show the line of code you would write to import JUST the `square` function from it.",
            "initial_code": "# Write the import line\n",
            "solution_code": "from math_plus import square\n",
            "test_cases": [{"input": "", "expected": ""}], # Logic check
        },
    },

    "les-modules-packages-3-intermediate": {
        "title": "Namespace Management",
        "content": """# Namespace Management

## 🎯 Learning Objectives
- Avoid name collisions with namespaces
- Understand the impact of `from module import *`
- Use the `dir()` function to inspect modules

## 📚 Concept Overview
When you use `import math`, `math` is a **namespace**. To get `pi`, you must use `math.pi`. This prevents your own `pi` variable from being overwritten.

### Why 'import *' is dangerous
`from math import *` brings EVERY name into your current scope. If you have your own function named `sin`, it will be replaced by math's `sin` without warning!

## 🏆 Key Takeaways
- Avoid `import *` in production code.
- Explicit imports make it clear where each function comes from.
""",
        "questions": [
            {"text": "Which function shows all the names currently defined in a module or scope?", "options": [
                {"text": "dir()", "correct": True}, {"text": "show()", "correct": False},
                {"text": "list_names()", "correct": False}, {"text": "vars()", "correct": False}]},
        ],
        "challenge": {
            "title": "Namespace Inspector",
            "description": "Import `math`. Print the list of all attributes and functions in `math` using `dir()`.",
            "initial_code": "import math\n# Print dir of math\n",
            "solution_code": "import math\nprint(dir(math))\n",
            "test_cases": [{"input": "", "expected": "*"}]
        },
    },

    "les-modules-packages-3-pro": {
        "title": "Compiled Modules (__pycache__)",
        "content": """# Compiled Modules (__pycache__)

## 🎯 Learning Objectives
- Understand what `.pyc` files are
- Learn how Python speeds up loading modules
- Understand when and why `__pycache__` is created

## 📚 Concept Overview
When you import a module, Python converts the source code into **Bytecode** and saves it in a `__pycache__` folder as a `.pyc` file.
Next time you run the script, Python loads the `.pyc` file directly, which is faster.

## 🏆 Key Takeaways
- `.pyc` files are NOT machine code; they are Python Bytecode.
- You can safely delete `__pycache__`; Python will just rebuild it next time.
""",
        "questions": [
            {"text": "What is stored in the `__pycache__` folder?", "options": [
                {"text": "Compiled bytecode (.pyc files)", "correct": True},
                {"text": "Temporary log files", "correct": False},
                {"text": "Backups of your code", "correct": False},
                {"text": "Your passwords", "correct": False}]},
        ],
        "challenge": {
            "title": "Bytecode Fact",
            "description": "Print 'Faster Loading' if you believe __pycache__ speeds up script execution, or 'Faster Start' if it only speeds up the time to start/import. (Technically it only speeds up the initialization phase).",
            "initial_code": "# Print choice\n",
            "solution_code": "print('Faster Start')\n",
            "test_cases": [{"input": "", "expected": "Faster Start"}],
        },
    },

    # ── Lesson 4: The if __name__ == "__main__": block ───────────────────────
    "les-modules-packages-4-beginner": {
        "title": "The Main Block Pattern",
        "content": """# The Main Block Pattern

## 🎯 Learning Objectives
- Protect your module's execution code
- Distinguish between "Importing" and "Running" a file
- Use `__name__` variable correctly

## 📚 Concept Overview
If you have `print("Hello")` at the top level of a file, it will run every time someone imports it! To prevent this, use:

```python
def main():
    print("This only runs if I start THIS file directly.")

if __name__ == "__main__":
    main()
```

## 🏆 Key Takeaways
- `__name__` is a special variable. It is set to `"__main__"` only when you run that specific file.
- This pattern allows a file to be both a reusable module and a standalone script.
""",
        "questions": [
            {"text": "What is the value of `__name__` when a file is imported as a module?", "options": [
                {"text": "The name of the file (e.g., 'utils')", "correct": True}, {"text": "'__main__'", "correct": False},
                {"text": "None", "correct": False}, {"text": "False", "correct": False}]},
            {"text": "Why do we use the `if __name__ == '__main__':` check?", "options": [
                {"text": "To prevent code from running when it's imported", "correct": True},
                {"text": "To make the code faster", "correct": False},
                {"text": "To hide functions from others", "correct": False},
                {"text": "It is required for every function", "correct": False}]},
        ],
        "challenge": {
            "title": "Main Checker",
            "description": "Print the current value of the `__name__` variable.",
            "initial_code": "# Print __name__\n",
            "solution_code": "print(__name__)\n",
            "test_cases": [{"input": "", "expected": "__main__"}],
        },
    },

    "les-modules-packages-4-intermediate": {
        "title": "Defining CLI Entry Points",
        "content": """# Defining CLI Entry Points

## 🎯 Learning Objectives
- Structure script logic for command-line usage
- Handle basic command line arguments with `sys.argv`
- Use the main block to parse inputs

## 📚 Concept Overview
```python
import sys

def main(args):
    print(f"Executing with {len(args)} arguments")

if __name__ == "__main__":
    main(sys.argv[1:]) # Skip the filename itself
```

## 🏆 Key Takeaways
- The main block is where you should put your user-facing logic or tests.
""",
        "questions": [
            {"text": "Which module and attribute contains the list of command line arguments passed to a script?", "options": [
                {"text": "sys.argv", "correct": True}, {"text": "os.args", "correct": False},
                {"text": "main.params", "correct": False}, {"text": "env.vars", "correct": False}]},
        ],
        "challenge": {
            "title": "Arg Counter",
            "description": "Import `sys`. In a main block, print the number of command line arguments (excluding the script name).",
            "initial_code": "import sys\n# Use sys.argv\n",
            "solution_code": "import sys\nif __name__ == '__main__':\n    print(len(sys.argv) - 1)\n",
            "test_cases": [{"input": "", "expected": "0"}],
        },
    },

    "les-modules-packages-4-pro": {
        "title": "Advanced __main__ with argparse",
        "content": """# Advanced __main__ with argparse

## 🎯 Learning Objectives
- Build professional CLI tools with `argparse`
- Define flags, help messages, and required inputs
- Understand the lifecycle of a script execution

## 📚 Concept Overview
`argparse` is a standard library module that makes it easy to write user-friendly command-line interfaces.

```python
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', type=int, nargs='+')
args = parser.parse_args()
print(sum(args.integers))
```

## ️🏆 Key Takeaways
- For complex scripts, always prefer `argparse` over manual `sys.argv` parsing.
""",
        "questions": [
            {"text": "Which standard library module is recommended for parsing complex command-line arguments?", "options": [
                {"text": "argparse", "correct": True}, {"text": "sys", "correct": False},
                {"text": "configparser", "correct": False}, {"text": "getopt", "correct": False}]},
        ],
        "challenge": {
            "title": "Simple Flag",
            "description": "Assume you use `argparse` and have a flag `--verbose`. Write the code to check if it's set and print 'Loud' if True.",
            "initial_code": "# code snippet for argparse check\n",
            "solution_code": "if args.verbose: print('Loud')\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    # ── Lesson 5: Packages and __init__.py ──────────────────────────────────
    "les-modules-packages-5-beginner": {
        "title": "Organizing into Packages",
        "content": """# Organizing into Packages

## 🎯 Learning Objectives
- Group multiple modules into a hierarchy
- Use the `.` notation for sub-modules
- Understand the role of `__init__.py`

## 📚 Concept Overview
A **Package** is just a folder that contains one or more Python modules.

### Structure
```text
my_project/
  utils/
    __init__.py
    math_tools.py
    string_tools.py
  main.py
```

### Importing from a Package
```python
from utils.math_tools import add
```

## 🏆 Key Takeaways
- Packages help manage massive projects by grouping related files.
- The `.` in `from a.b import c` indicates a folder/file path.
""",
        "questions": [
            {"text": "What special file is used (traditionally) to tell Python that a directory should be treated as a package?", "options": [
                {"text": "__init__.py", "correct": True}, {"text": "package.py", "correct": False},
                {"text": "main.py", "correct": False}, {"text": "__main__.py", "correct": False}]},
            {"text": "In `import sound.effects.echo`, what is 'echo' likely to be?", "options": [
                {"text": "A module (.py file) inside the 'effects' package", "correct": True},
                {"text": "A variable", "correct": False},
                {"text": "A class", "correct": False},
                {"text": "A built-in function", "correct": False}]},
        ],
        "challenge": {
            "title": "Package Import",
            "description": "Show the line of code to import the function `log` from a module `logger` inside a package `utils`.",
            "initial_code": "# Write the import\n",
            "solution_code": "from utils.logger import log\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-modules-packages-5-intermediate": {
        "title": "Relative Imports",
        "content": """# Relative Imports

## 🎯 Learning Objectives
- Use relative paths within a package (`.` and `..`)
- Understand why relative imports are mostly for library development
- Resolve "ImportError: attempted relative import with no known parent package"

## 📚 Concept Overview
Inside a package, you can refer to sibling modules using dots.

```python
# Inside utils.math_tools
from .string_tools import capitalize # Same directory
from ..core import logic            # Parent directory
```

## ⚠️ Common Pitfalls
- Running a file with relative imports directly (instead of through `python -m`). This will ALWAYS fail.

## 🏆 Key Takeaways
- Relative imports make a package "portable" because you can rename the root folder without changing internal imports.
""",
        "questions": [
            {"text": "What does a single dot `.` represent in a relative import?", "options": [
                {"text": "The current package directory", "correct": True}, {"text": "The parent directory", "correct": False},
                {"text": "The project root", "correct": False}, {"text": "The system root", "correct": False}]},
        ],
        "challenge": {
            "title": "Sibling Import",
            "description": "Inside `pkg.mod1`, write a relative import for `mod2` from the same package.",
            "initial_code": "# Use dots\n",
            "solution_code": "from . import mod2\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-modules-packages-5-pro": {
        "title": "The __all__ Variable",
        "content": """# The __all__ Variable

## 🎯 Learning Objectives
- Control what gets exported in `from module import *`
- Use `__all__` to define your module's public API
- Manage hidden internal names

## 📚 Concept Overview
If you define `__all__` at the top of your file, only those names will be imported if someone uses the "import star" syntax.

```python
__all__ = ["start", "stop"]

def start(): pass
def stop(): pass
def _internal(): pass # Hidden by convention and by __all__
```

## 🏆 Key Takeaways
- `__all__` is an explicit list of your module's public features.
- It is a best practice for high-quality, professional libraries.
""",
        "questions": [
            {"text": "What type of object should `__all__` be in a Python module?", "options": [
                {"text": "A list of strings", "correct": True}, {"text": "A dictionary", "correct": False},
                {"text": "A single string", "correct": False}, {"text": "A boolean", "correct": False}]},
        ],
        "challenge": {
            "title": "Public API",
            "description": "Define `__all__` so that only functions `run` and `walk` are exported. (Assume functions exist).",
            "initial_code": "# Set __all__\n",
            "solution_code": "__all__ = ['run', 'walk']\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },
}

class Command(BaseCommand):
    help = "Hydrate Module 5 (Modules & Packages) — Lessons 1-5"

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
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Hydrated {count} lessons in Module 5 (1-5)"))
