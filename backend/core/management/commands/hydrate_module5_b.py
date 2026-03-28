"""python manage.py hydrate_module5_b -- Module 5 Modules & Packages Lessons 6-10"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Lesson, Quiz, Question, Challenge

LESSONS = {
    # ── Lesson 6: Built-in vs External Modules ──────────────────────────────
    "les-modules-packages-6-beginner": {
        "title": "Built-in vs External Modules",
        "content": """# Built-in vs External Modules

## 🎯 Learning Objectives
- Differentiate between standard library and external packages
- Understand the role of PyPI (Python Package Index)
- Learn why external libraries are a core part of Python development

## 📚 Concept Overview
- **Standard Library**: Modules that come pre-installed with Python (e.g., `math`, `sys`).
- **External Packages**: Modules created by other developers and hosted on PyPI (e.g., `requests`, `numpy`, `pandas`).

To use an external package, you first have to download it using a tool called `pip`.

## 🏆 Key Takeaways
- Over 500,000 packages exist on PyPI.
- Using external packages is what makes Python powerful for data science, web development, and AI.
""",
        "questions": [
            {"text": "What is PyPI?", "options": [
                {"text": "The Python Package Index (a repository for external packages)", "correct": True},
                {"text": "A specialized version of Python for Raspberry Pi", "correct": False},
                {"text": "A mathematical constant module", "correct": False},
                {"text": "A built-in text editor", "correct": False}]},
            {"text": "Which of these is likely an external package rather than a built-in one?", "options": [
                {"text": "pandas", "correct": True}, {"text": "math", "correct": False},
                {"text": "random", "correct": False}, {"text": "sys", "correct": False}]},
        ],
        "challenge": {
            "title": "Module Trivia",
            "description": "True or False: You need to install the 'math' module before using it in your script. Print 'True' or 'False'.",
            "initial_code": "# Type your answer\n",
            "solution_code": "print('False')\n",
            "test_cases": [{"input": "", "expected": "False"}],
        },
    },

    "les-modules-packages-6-intermediate": {
        "title": "The PyPI Website & Documentation",
        "content": """# The PyPI Website & Documentation

## 🎯 Learning Objectives
- Learn how to search for packages on PyPI
- Understand versioning (Semantic Versioning)
- Read package health metrics (last updated, stars, etc.)

## 📚 Concept Overview
When choosing a package, look for:
1. **Recent updates**: Avoid abandoned libraries.
2. **Download count**: Indicates popularity and community support.
3. **Documentation**: Is it clear and updated?

### Semantic Versioning (SemVer)
Version numbers like `2.5.1`:
- `2`: Major (Breaking changes)
- `5`: Minor (New features, no breakage)
- `1`: Patch (Bug fixes)

## 🏆 Key Takeaways
- Researching a library before using it saves hours of future debugging.
""",
        "questions": [
            {"text": "In a version number like 1.4.2, what does the first number (1) represent?", "options": [
                {"text": "Major version (potential breaking changes)", "correct": True},
                {"text": "Minor version (new features)", "correct": False},
                {"text": "The number of files", "correct": False},
                {"text": "Patch version (bug fixes)", "correct": False}]},
        ],
        "challenge": {
            "title": "SemVer Check",
            "description": "Read two version strings '2.1.0' and '3.0.0'. Print 'Major Change' if the first number is different, else 'Safe Change'.",
            "initial_code": "# Simple version compare\n",
            "solution_code": "v1 = input().split('.')\nv2 = input().split('.')\nprint('Major Change' if v1[0] != v2[0] else 'Safe Change')\n",
            "test_cases": [{"input": "2.1.0\n3.0.0", "expected": "Major Change"}, {"input": "1.5.0\n1.6.0", "expected": "Safe Change"}],
        },
    },

    "les-modules-packages-6-pro": {
        "title": "Source Distribution vs Wheels",
        "content": """# Source Distribution vs Wheels

## 🎯 Learning Objectives
- Understand the difference between `sdist` and `.whl` files
- Learn how `pip` handles binary distributions
- Understand why some packages require a C-compiler during installation

## 📚 Concept Overview
- **sdist (Source Distribution)**: Raw source code. If it includes C extensions, your computer must compile them.
- **Wheels (.whl)**: Pre-compiled binaries. Much faster to install and doesn't require extra tools.

## 🏆 Key Takeaways
- Prefer `wheels` for fast and trouble-free installations.
- `pip` automatically prefers wheels if they match your system architecture.
""",
        "questions": [
            {"text": "What is a Python 'Wheel'?", "options": [
                {"text": "A pre-compiled binary distribution format", "correct": True},
                {"text": "A tool to rotate logs", "correct": False},
                {"text": "A type of loop", "correct": False},
                {"text": "A data structure", "correct": False}]},
        ],
        "challenge": {
            "title": "Whl vs Tar",
            "description": "Assume you have two files: 'numpy-1.21.0.whl' (Wheel) and 'numpy-1.21.0.tar.gz' (Source). Which one is typically faster to install? Print the file extension (.whl or .tar.gz).",
            "initial_code": "# Answer format: .ext\n",
            "solution_code": "print('.whl')\n",
            "test_cases": [{"input": "", "expected": ".whl"}],
        },
    },

    # ── Lesson 7: Virtual Environments (venv) ───────────────────────────────
    "les-modules-packages-7-beginner": {
        "title": "What is a Virtual Environment?",
        "content": """# What is a Virtual Environment?

## 🎯 Learning Objectives
- Understand why global installations are dangerous
- Isolate project dependencies
- Learn the purpose of the `venv` module

## 📚 Concept Overview
A **Virtual Environment** is a separate, isolated copy of Python for a specific project. This prevents "Dependency Hell" where project A requires `requests 1.0` and project B requires `requests 2.0`.

```bash
# Create one
python -m venv .venv
```

## 🏆 Key Takeaways
- Every project should have its own virtual environment.
- Never install project-specific libraries globally!
""",
        "questions": [
            {"text": "Why should you use a virtual environment?", "options": [
                {"text": "To prevent version conflicts between different projects", "correct": True},
                {"text": "To make Python run faster", "correct": False},
                {"text": "To hide your code", "correct": False},
                {"text": "To encrypt your project", "correct": False}]},
            {"text": "Which built-in module creates virtual environments?", "options": [
                {"text": "venv", "correct": True}, {"text": "virtualenv", "correct": False},
                {"text": "environment", "correct": False}, {"text": "isolate", "correct": False}]},
        ],
        "challenge": {
            "title": "Venv Command",
            "description": "Write the exact bash command to create a virtual environment named 'myenv' using the built-in python module.",
            "initial_code": "# Write command\n",
            "solution_code": "python -m venv myenv\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-modules-packages-7-intermediate": {
        "title": "Activation & Deactivation",
        "content": """# Activation & Deactivation

## 🎯 Learning Objectives
- Activate sub-environments on Windows, Mac, and Linux
- Distinguish between a created and an active environment
- Deactivate an environment safely

## 📚 Concept Overview
| OS | Command |
|----|---------|
| Windows (CMD) | `.venv\\Scripts\\activate` |
| Windows (PS) | `.venv\\Scripts\\Activate.ps1` |
| Mac/Linux | `source .venv/bin/activate` |

Once activated, your terminal will usually show `(.venv)` next to the prompt.

## 🏆 Key Takeaways
- Creating is not enough; you must **activate** it to use it.
- Typing `deactivate` returns you to the global Python.
""",
        "questions": [
            {"text": "On Linux or Mac, what is the command to activate a venv in the '.venv' folder?", "options": [
                {"text": "source .venv/bin/activate", "correct": True}, {"text": ".venv\\Scripts\\activate", "correct": False},
                {"text": "python .venv start", "correct": False}, {"text": "env start", "correct": False}]},
        ],
        "challenge": {
            "title": "Prompt Check",
            "description": "If your terminal prompt shows `(.venv) user@machine:~$`, is the virtual environment active? Print 'Yes' or 'No'.",
            "initial_code": "# Logical check\n",
            "solution_code": "print('Yes')\n",
            "test_cases": [{"input": "", "expected": "Yes"}],
        },
    },

    "les-modules-packages-7-pro": {
        "title": "Internal Mechanics of Venv",
        "content": """# Internal Mechanics of Venv

## 🎯 Learning Objectives
- Understand how `bin/python` symlinks or copies work
- Learn about `pyvenv.cfg` configuration
- Master the `prefix` vs `global_prefix` variables

## 📚 Concept Overview
A virtual environment doesn't copy the entire Python exe (usually). Instead, it creates a config file that tells the child processes where to look for libraries.

When active, `sys.prefix` points to the folder of your venv, while `sys.base_prefix` points to the main installation.

## 🏆 Key Takeaways
- Virtual environments are Lightweight; they are mostly just clever configuration and some scripts.
""",
        "questions": [
            {"text": "Which `sys` attribute points to the current active environment's root?", "options": [
                {"text": "sys.prefix", "correct": True}, {"text": "sys.path", "correct": False},
                {"text": "sys.base_prefix", "correct": False}, {"text": "sys.home", "correct": False}]},
        ],
        "challenge": {
            "title": "Prefix Compare",
            "description": "Import `sys`. Print 'Active' if `sys.prefix` is NOT equal to `sys.base_prefix`, otherwise 'Global'.",
            "initial_code": "import sys\n# Check if in venv\n",
            "solution_code": "import sys\nprint('Active' if sys.prefix != sys.base_prefix else 'Global')\n",
            "test_cases": [{"input": "", "expected": "*"}],
        },
    },

    # ── Lesson 8: Pip & Dependency Management ────────────────────────────────
    "les-modules-packages-8-beginner": {
        "title": "The Pip Tool",
        "content": """# The Pip Tool

## 🎯 Learning Objectives
- Install packages using `pip install`
- View installed packages using `pip list`
- Uninstall packages safely

## 📚 Concept Overview
`pip` (Package Installer for Python) is the standard tool.

```bash
pip install requests
pip list
pip uninstall requests
```

## ️🏆 Key Takeaways
- `pip` handles downloading, versions, and dependencies of external libraries.
""",
        "questions": [
            {"text": "What command installs a package named 'flask'?", "options": [
                {"text": "pip install flask", "correct": True}, {"text": "get flask", "correct": False},
                {"text": "python get flask", "correct": False}, {"text": "pip download flask", "correct": False}]},
        ],
        "challenge": {
            "title": "Listing Command",
            "description": "Show the bash command to see all currently installed packages in your environment.",
            "initial_code": "# Pip list\n",
            "solution_code": "pip list\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-modules-packages-8-intermediate": {
        "title": "Requirements Files",
        "content": """# Requirements Files

## 🎯 Learning Objectives
- Create a `requirements.txt` using `pip freeze`
- Install all project dependencies at once
- Understand pinned versions (e.g., `requests==2.25.1`)

## 📚 Concept Overview
To share your project with others, you should never share the venv folder. Instead, share a list of names.

```bash
# Save your list
pip freeze > requirements.txt

# Install from a list
pip install -r requirements.txt
```

## 🏆 Key Takeaways
- `requirements.txt` is the ID card of your project's dependencies.
""",
        "questions": [
            {"text": "Which pip command displays your installed packages in the format used for requirements files?", "options": [
                {"text": "pip freeze", "correct": True}, {"text": "pip list", "correct": False},
                {"text": "pip requirements", "correct": False}, {"text": "pip show", "correct": False}]},
            {"text": "How do you install everything from a file called 'deps.txt'?", "options": [
                {"text": "pip install -r deps.txt", "correct": True}, {"text": "pip load deps.txt", "correct": False},
                {"text": "pip get all deps.txt", "correct": False}, {"text": "python install deps.txt", "correct": False}]},
        ],
        "challenge": {
            "title": "Version Pinner",
            "description": "Write a line for a requirements file that pins 'Django' specifically to version '4.2'.",
            "initial_code": "# Pin Django\n",
            "solution_code": "Django==4.2\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-modules-packages-8-pro": {
        "title": "Advanced Tools (Pipenv, Poetry)",
        "content": """# Advanced Tools (Pipenv, Poetry)

## 🎯 Learning Objectives
- Understand modern package managers
- Learn about `lock` files and deterministic builds
- Compare Poetry vs Pip

## 📚 Concept Overview
Modern tools like **Poetry** use a `pyproject.toml` file to manage everything (building, dependencies, publishing). They create a `lock` file to ensure that every developer has EXACTLY the same sub-dependencies.

## 🏆 Key Takeaways
- `requirements.txt` is basic; `Poetry` is professional and powerful for modern workflows.
""",
        "questions": [
            {"text": "Which of these is a modern dependency manager that uses `pyproject.toml`?", "options": [
                {"text": "Poetry", "correct": True}, {"text": "Pip 1.0", "correct": False},
                {"text": "EasyInstall", "correct": False}, {"text": "SetupPy", "correct": False}]},
        ],
        "challenge": {
            "title": "Lock File Fact",
            "description": "Print 'Yes' if lock files help ensure everyone has the same versions of nested/sub dependencies.",
            "initial_code": "# Boolean fact\n",
            "solution_code": "print('Yes')\n",
            "test_cases": [{"input": "", "expected": "Yes"}],
        },
    },

    # ── Lesson 9: Project Structure Best Practices ───────────────────────────
    "les-modules-packages-9-beginner": {
        "title": "Standard Project Layout",
        "content": """# Standard Project Layout

## 🎯 Learning Objectives
- Layout a professional project folder
- Separate source code from tests and docs
- Use the `src/` layout pattern

## 📚 Concept Overview
```text
my_awesome_app/
  docs/
  src/
    app/
      __init__.py
      main.py
  tests/
  .gitignore
  README.md
  requirements.txt
```

## 🏆 Key Takeaways
- Clean organization makes collaboration much easier.
""",
        "questions": [
            {"text": "What is the conventional folder name for source code in many Python projects?", "options": [
                {"text": "src", "correct": True}, {"text": "code", "correct": False},
                {"text": "scripts", "correct": False}, {"text": "bin", "correct": False}]},
        ],
        "challenge": {
            "title": "Readme Check",
            "description": "Print the conventional name for the documentation file that describes how to use your project.",
            "initial_code": "# Convention check\n",
            "solution_code": "print('README.md')\n",
            "test_cases": [{"input": "", "expected": "README.md"}],
        },
    },

    "les-modules-packages-9-intermediate": {
        "title": ".gitignore Essentials",
        "content": """# .gitignore Essentials

## 🎯 Learning Objectives
- Protect sensitive data from Git
- Avoid committing binary or temporary files
- List standard Python ignore patterns

## 📚 Concept Overview
You should NEVER commit these to Github:
- `.venv/` (too large, platform specific)
- `__pycache__/`
- `.env` (contains secret passwords/API keys)
- `.DS_Store` (system junk)

## 🏆 Key Takeaways
- A good `.gitignore` keeps your repository clean and safe.
""",
        "questions": [
            {"text": "Should you commit your virtual environment folder? (.venv)", "options": [
                {"text": "No", "correct": True}, {"text": "Yes", "correct": False},
                {"text": "Only if using Docker", "correct": False}, {"text": "Only for small projects", "correct": False}]},
        ],
        "challenge": {
            "title": "Ignore List",
            "description": "List the TWO folders most commonly ignored in Python projects space-separated. (Hint: venv and cache stuff).",
            "initial_code": "# List two patterns\n",
            "solution_code": "print('.venv __pycache__')\n",
            "test_cases": [{"input": "", "expected": ".venv __pycache__"}],
        },
    },

    "les-modules-packages-9-pro": {
        "title": "Setuptools & pyproject.toml",
        "content": """# Setuptools & pyproject.toml

## 🎯 Learning Objectives
- Configure your project as a distributable package
- Understand the shift from `setup.py` to `pyproject.toml`
- Add entry points (scripts) to your package

## 📚 Concept Overview
If you want someone to be able to do `pip install my-app`, you need a configuration file that describes your package version, name, and dependencies.

Modern standard: **PEP 518** and **PEP 621**.

## 🏆 Key Takeaways
- `pyproject.toml` is the new unified config for Python packaging.
""",
        "questions": [
            {"text": "What is the modern, unified configuration file for Python projects?", "options": [
                {"text": "pyproject.toml", "correct": True}, {"text": "setup.cfg", "correct": False},
                {"text": "manifest.in", "correct": False}, {"text": "config.yaml", "correct": False}]},
        ],
        "challenge": {
            "title": "Metadata Check",
            "description": "Print 'True' if pyproject.toml can replace many older files like setup.py, requirements.txt, and flake8 config.",
            "initial_code": "# Capability check\n",
            "solution_code": "print('True')\n",
            "test_cases": [{"input": "", "expected": "True"}],
        },
    },

    # ── Lesson 10: Mini Project ──────────────────────────────────────────────
    "les-modules-packages-10-beginner": {
        "title": "Project: Simple Logger Library",
        "content": """# Project: Simple Logger Library

## 🎯 Goal
Build a directory with two files.
- `logger.py`: Contains functions `info(msg)` and `error(msg)`.
- `main.py`: Imports and uses the logger.

## 📝 Steps
1. Create `logger.py`.
2. Implement date-stamped printing.
3. Use it in `main.py`.
""",
        "questions": [],
        "challenge": {
            "title": "Logger Call",
            "description": "Given `logger.py` has `log(x)`, write the code (2 lines) to import it and call it with 'Done'.",
            "initial_code": "# Import and call\n",
            "solution_code": "import logger\nlogger.log('Done')\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-modules-packages-10-intermediate": {
        "title": "Project: Modular Converter",
        "content": """# Project: Modular Converter

## 🎯 Goal
Create a package `converters` with two modules: `temp.py` and `length.py`.

## 📝 Requirements
- Use namespaces correctly.
- Add a main block to `temp.py` for testing.
""",
        "questions": [],
        "challenge": {
            "title": "Package Structure",
            "description": "If you have `converters/temp.py`, show the CORRECT import line to use the `c_to_f` function from `main.py` (outside the folder).",
            "initial_code": "# Deep import\n",
            "solution_code": "from converters.temp import c_to_f\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-modules-packages-10-pro": {
        "title": "Project: Package Distributor",
        "content": """# Project: Package Distributor

## 🎯 Goal
Simulate the steps to publish a package.
1. Organize into `src/` layout.
2. Create `pyproject.toml`.
3. Build a wheel.
""",
        "questions": [],
        "challenge": {
            "title": "Build Tool",
            "description": "What official Python command tool is used to build distribution packages from a project folder? (Hint: it starts with 'b')",
            "initial_code": "# Tool name\n",
            "solution_code": "print('build')\n",
            "test_cases": [{"input": "", "expected": "build"}],
        },
    },
}

class Command(BaseCommand):
    help = "Hydrate Module 5 (Modules & Packages) — Lessons 6-10"

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
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Hydrated {count} lessons in Module 5 (6-10)"))
