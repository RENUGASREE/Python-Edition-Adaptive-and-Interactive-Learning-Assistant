"""python manage.py hydrate_module10 -- Module 10 Projects Lessons 1-5"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Lesson, Quiz, Question, Challenge

LESSONS = {
    # ── Lesson 1: CLI Application: To-Do List ────────────────────────────────
    "les-real-world-projects-1-beginner": {
        "title": "Building a CLI To-Do List",
        "content": """# Building a CLI To-Do List

## 🎯 Goal
Combine basic input, lists, and loops to build a functional Task Manager.

## 📝 Project Architecture
1. **Data Store**: Use a simple Python List `tasks = []`.
2. **Main Loop**: Use `while True` to keep the program running.
3. **User Choice**: Use `input()` to get Commands (add, view, remove, exit).

```python
tasks = []
while True:
    choice = input("1. Add 2. View 3. Exit: ")
    if choice == '1':
        t = input("Task: ")
        tasks.append(t)
    elif choice == '2':
        print(tasks)
    elif choice == '3':
        break
```

## 🏆 Key Takeaways
- CLI apps are the first step in building real tools.
- Proper input validation is key to a good user experience.
""",
        "questions": [
            {"text": "Which data structure is most suitable for storing an ordered list of tasks?", "options": [
                {"text": "List", "correct": True}, {"text": "Set", "correct": False},
                {"text": "Dictionary", "correct": False}, {"text": "Integer", "correct": False}]},
            {"text": "How do you keep a CLI program running until the user says stop?", "options": [
                {"text": "Using a while True loop", "correct": True},
                {"text": "Using a for loop", "correct": False},
                {"text": "Using an if statement", "correct": False},
                {"text": "Using a try-except block", "correct": False}]},
        ],
        "challenge": {
            "title": "Task Adder",
            "description": "Initialize `tasks = []`. Append 'Code' and 'Eat' to it. Print the number of tasks.",
            "initial_code": "tasks = []\n# add tasks\n",
            "solution_code": "tasks = []\ntasks.append('Code')\ntasks.append('Eat')\nprint(len(tasks))\n",
            "test_cases": [{"input": "", "expected": "2"}],
        },
    },

    "les-real-world-projects-1-intermediate": {
        "title": "Managing Tasks with Enums",
        "content": """# Managing Tasks with Enums

## 🎯 Goal
Improve the 'To-Do' list by using `Enum` for task status (OPEN, CLOSED, BLOCKED).

## 📚 Concept Overview
Using strings like "Open" is risky because of typos. `Enum` provides a safe way to define constant options.

```python
from enum import Enum

class Status(Enum):
    OPEN = 1
    CLOSED = 2
```

## 🏆 Key Takeaways
- Enums make your code more robust and self-documenting.
""",
        "questions": [
            {"text": "Why use Enums instead of plain strings for status?", "options": [
                {"text": "They prevent typos and provide a fixed set of allowed values", "correct": True},
                {"text": "They make the code run faster", "correct": False},
                {"text": "They automatically save to the disk", "correct": False},
                {"text": "They are required by the OS", "correct": False}]},
        ],
        "challenge": {
            "title": "Status Check",
            "description": "Define Enum `S` with `O=1`. Print 'Correct' if `S.O == S.O` is True.",
            "initial_code": "from enum import Enum\n# setup Enum\n",
            "solution_code": "from enum import Enum\nclass S(Enum): O=1\nif S.O == S.O: print('Correct')\n",
            "test_cases": [{"input": "", "expected": "Correct"}],
        },
    },

    "les-real-world-projects-1-pro": {
        "title": "To-Do List with Persistence",
        "content": """# To-Do List with Persistence

## 🎯 Goal
Modify the CLI app to save tasks to a file automatically.

## 📝 Features
- Load tasks from `tasks.txt` on startup.
- Save to `tasks.txt` whenever a task is added.
- Handle `FileNotFoundError` if the file doesn't exist yet.

```python
def load_tasks():
    try:
        with open("tasks.txt", "r") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return []
```

## 🏆 Key Takeaways
- Persistence is what turns a script into an actual application.
""",
        "questions": [
            {"text": "Which exception should you catch if the storage file doesn't exist yet?", "options": [
                {"text": "FileNotFoundError", "correct": True}, {"text": "IOError", "correct": False},
                {"text": "ValueError", "correct": False}, {"text": "NameError", "correct": False}]},
        ],
        "challenge": {
            "title": "Line Loader",
            "description": "Write a function `save(items)` that writes each item to 'out.txt' on a new line.",
            "initial_code": "def save(items):\n    # write using with\n",
            "solution_code": "def save(items):\n    with open('out.txt', 'w') as f:\n        for i in items: f.write(str(i) + '\\n')\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    # ── Lesson 2: Web Scraper Basics ─────────────────────────────────────────
    "les-real-world-projects-2-beginner": {
        "title": "Introduction to Web Scraping",
        "content": """# Introduction to Web Scraping

## 🎯 Goal
Understand how to pull data from any website using Python.

## 🛠️ The Toolkit
1. **Requests**: Used to download the HTML.
2. **BeautifulSoup (bs4)**: Used to search the HTML (like finding all `<h1>` tags).

```python
import requests
from bs4 import BeautifulSoup

url = "https://example.com"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
print(soup.title.text)
```

## 🏆 Key Takeaways
- Web scraping is essentially "Browser Automation" without the UI.
- Always check a site's `robots.txt` before scraping.
""",
        "questions": [
            {"text": "Which library is used to send HTTP requests in Python?", "options": [
                {"text": "requests", "correct": True}, {"text": "bs4", "correct": False},
                {"text": "os", "correct": False}, {"text": "sys", "correct": False}]},
            {"text": "What is BeautifulSoup used for?", "options": [
                {"text": "Parsing and navigating HTML/XML documents", "correct": True},
                {"text": "Sending emails", "correct": False},
                {"text": "Running a local server", "correct": False},
                {"text": "Calculating math", "correct": False}]},
        ],
        "challenge": {
            "title": "Status Code",
            "description": "Use `requests.get('https://google.com')` and print the `status_code`.",
            "initial_code": "import requests\n# get status\n",
            "solution_code": "import requests\nres = requests.get('https://google.com')\nprint(res.status_code)\n",
            "test_cases": [{"input": "", "expected": "200"}],
        },
    },

    "les-real-world-projects-2-intermediate": {
        "title": "Finding Data in HTML",
        "content": """# Finding Data in HTML

## 🎯 Goal
Extract specific elements using CSS selectors and tags.

## 📚 Concept Overview
```python
# Find all links
links = soup.find_all("a")

# Find by ID
header = soup.find(id="main-title")

# Find by Class
items = soup.find_all("li", class_="product-item")
```

## 🏆 Key Takeaways
- Use Developer Tools (F12) in your browser to inspect the HTML structure before writing your script.
""",
        "questions": [
            {"text": "Which method returns a LIST of all matching tags?", "options": [
                {"text": "find_all()", "correct": True}, {"text": "find()", "correct": False},
                {"text": "get_all()", "correct": False}, {"text": "select_one()", "correct": False}]},
        ],
        "challenge": {
            "title": "Title Grabber",
            "description": "Assume `soup` is defined. Print the text inside the `<h1>` tag.",
            "initial_code": "# print h1 text\n",
            "solution_code": "print(soup.find('h1').text)\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-real-world-projects-2-pro": {
        "title": "Building a News Scraper",
        "content": """# Building a News Scraper

## 🎯 Goal
Scrape a news site and save the headlines to a JSON file.

## 📝 Project Steps
1. Request page.
2. Find all headline tags (e.g., `<h3>`).
3. Store in a list of dictionaries: `[{"title": "...", "link": "..."}]`.
4. Export using `json.dump()`.

## ⚠️ Common Pitfalls
- **Rate Limiting**: Don't send 1000 requests in 1 second or you might get banned! Use `time.sleep()`.
""",
        "questions": [
            {"text": "What is 'Rate Limiting'?", "options": [
                {"text": "The restriction of the number of requests a user can make to a server in a given timeframe", "correct": True},
                {"text": "Calculating the speed of light", "correct": False},
                {"text": "Managing database storage", "correct": False},
                {"text": "Encrypting the server", "correct": False}]},
        ],
        "challenge": {
            "title": "JSON Exporter",
            "description": "Given `data = {'val': 1}`. Write it to 'data.json' using `json.dump`.",
            "initial_code": "import json\ndata = {'val': 1}\n# dump to file\n",
            "solution_code": "import json\ndata = {'val': 1}\nwith open('data.json', 'w') as f:\n    json.dump(data, f)\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    # ── Lesson 3: Data Formatter (JSON/CSV) ──────────────────────────────────
    "les-real-world-projects-3-beginner": {
        "title": "Processing CSV Data",
        "content": """# Processing CSV Data

## 🎯 Goal
Read and write spreadsheet-like data using the `csv` module.

## 📚 Concept Overview
```python
import csv

with open("data.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row) # row is a list of strings
```

## 🏆 Key Takeaways
- `csv.reader` returns lists; `csv.DictReader` returns dictionaries.
""",
        "questions": [
            {"text": "Which module is built into Python for handling comma-separated values?", "options": [
                {"text": "csv", "correct": True}, {"text": "spreadsheet", "correct": False},
                {"text": "json", "correct": False}, {"text": "excel", "correct": False}]},
        ],
        "challenge": {
            "title": "CSV Row Count",
            "description": "Read 'data.csv' and print the total number of rows.",
            "initial_code": "import csv\n# count rows\n",
            "solution_code": "import csv\nwith open('data.csv', 'r') as f:\n    print(len(list(csv.reader(f))))\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-real-world-projects-3-intermediate": {
        "title": "JSON to CSV Converter",
        "content": """# JSON to CSV Converter

## 🎯 Goal
Build a utility script that transforms JSON data into a CSV file.

## 📝 Logic Flow
1. Load JSON using `json.load()`.
2. Extract the list of objects.
3. Get headers from the keys of the first object.
4. Write using `csv.DictWriter`.

```python
with open("out.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerows(list_of_dicts)
```

## 🏆 Key Takeaways
- Converting data formats is a primary task for Python in backend development.
""",
        "questions": [
            {"text": "Which class helps you write rows directly from Python dictionaries into a CSV?", "options": [
                {"text": "csv.DictWriter", "correct": True}, {"text": "csv.ListWriter", "correct": False},
                {"text": "csv.TableWriter", "correct": False}, {"text": "csv.MapWriter", "correct": False}]},
        ],
        "challenge": {
            "title": "Key Picker",
            "description": "Given `d = {'a': 1, 'b': 2}`. Extract the keys as a list and print it.",
            "initial_code": "d = {'a': 1, 'b': 2}\n# list keys\n",
            "solution_code": "d = {'a': 1, 'b': 2}\nprint(list(d.keys()))\n",
            "test_cases": [{"input": "", "expected": "['a', 'b']"}],
        },
    },

    "les-real-world-projects-3-pro": {
        "title": "Handling Large Data with Pandas",
        "content": """# Handling Large Data with Pandas

## 🎯 Goal
Introduction to the industrial-strength library for data analysis.

## 📚 Concept Overview
While `csv` is great for small files, **Pandas** is the standard for Big Data.

```python
import pandas as pd
df = pd.read_csv("large_data.csv")
print(df.describe()) # Instant stats!
```

## 🏆 Key Takeaways
- Pandas turns CSVs into a "DataFrame" (like an Excel sheet in RAM).
- It is much faster than manual looping for calculation.
""",
        "questions": [
            {"text": "Which third-party library is considered the industry standard for data manipulation in Python?", "options": [
                {"text": "Pandas", "correct": True}, {"text": "Requests", "correct": False},
                {"text": "Math", "correct": False}, {"text": "Os", "correct": False}]},
        ],
        "challenge": {
            "title": "Pandas Import",
            "description": "What is the standard convention for importing the pandas library? Print the import line.",
            "initial_code": "# import line\n",
            "solution_code": "print('import pandas as pd')\n",
            "test_cases": [{"input": "", "expected": "import pandas as pd"}],
        },
    },

    # ── Lesson 4: Password Manager ───────────────────────────────────────────
    "les-real-world-projects-4-beginner": {
        "title": "Project: Password Vault",
        "content": """# Project: Password Vault

## 🎯 Goal
Build a local vault that stores service names and passwords.

## 📝 Features
- `add`: Saves service/password.
- `get`: Retrieves password for a service.
- Data stored in a dictionary and saved to JSON.
""",
        "questions": [],
        "challenge": {
            "title": "Vault Add",
            "description": "Update dictionary `v = {}` with key 'fb' and value '123'. Print the dict.",
            "initial_code": "v = {}\n# update\n",
            "solution_code": "v = {'fb': '123'}\nprint(v)\n",
            "test_cases": [{"input": "", "expected": "{'fb': '123'}"}],
        },
    },

    "les-real-world-projects-4-intermediate": {
        "title": "Securing the Vault",
        "content": """# Securing the Vault

## 🎯 Goal
Add a 'Master Password' that guards access to the program.

## 📝 Logic
At the start of the script:
```python
master = input("Master Password: ")
if master != "SECRET":
    print("Denied")
    exit()
```

## ⚠️ Security Note
In a real app, you would never store passwords in plain text! You would use **Encryption** (like the `cryptography` library).
""",
        "questions": [
            {"text": "Which function should you use to stop the program immediately if access is denied?", "options": [
                {"text": "exit()", "correct": True}, {"text": "stop()", "correct": False},
                {"text": "end()", "correct": False}, {"text": "break", "correct": False}]},
        ],
        "challenge": {
            "title": "Access Loop",
            "description": "Write an if-statement that checks if `p == '123'`. If yes, print 'OK', else 'No'.",
            "initial_code": "p = '123'\n# check\n",
            "solution_code": "p = '123'\nif p == '123': print('OK')\nelse: print('No')\n",
            "test_cases": [{"input": "", "expected": "OK"}],
        },
    },

    "les-real-world-projects-4-pro": {
        "title": "Encryption with Cryptography",
        "content": """# Encryption with Cryptography

## 🎯 Goal
Actually encrypt the password file so no one can read it with Notepad.

## 📚 Tools
`Fernet` from the `cryptography.fernet` module.

```python
from cryptography.fernet import Fernet
key = Fernet.generate_key()
f = Fernet(key)
token = f.encrypt(b"secret message")
```

## 🏆 Key Takeaways
- Encryption transforms data into "Cyphertext" that is unreadable without a key.
""",
        "questions": [
            {"text": "What is the result of encryption called?", "options": [
                {"text": "Cyphertext", "correct": True}, {"text": "Plaintext", "correct": False},
                {"text": "Metadata", "correct": False}, {"text": "Bytecode", "correct": False}]},
        ],
        "challenge": {
            "title": "Byte Check",
            "description": "Encryption usually requires bytes. Convert 'hello' string to bytes and print the result.",
            "initial_code": "s = 'hello'\n# convert\n",
            "solution_code": "s = 'hello'\nprint(s.encode())\n",
            "test_cases": [{"input": "", "expected": "b'hello'"}],
        },
    },

    # ── Lesson 5: Inventory System (OOP) ─────────────────────────────────────
    "les-real-world-projects-5-beginner": {
        "title": "OOP Inventory: The Item Class",
        "content": """# OOP Inventory: The Item Class

## 🎯 Goal
Build the foundation of an inventory tracker.

```python
class Item:
    def __init__(self, name, price, qty):
        self.name = name
        self.price = price
        self.qty = qty
    
    def total_value(self):
        return self.price * self.qty
```

## 🏆 Key Takeaways
- Classes help group related attributes (name, price) and behavior (calculating value) together.
""",
        "questions": [],
        "challenge": {
            "title": "Value Calc",
            "description": "Item(price=10, qty=5). Print the result of `total_value()`.",
            "initial_code": "class Item:\n    def __init__(self, p, q): self.p, self.q = p, q\n    def calc(self): return self.p * self.q\n",
            "solution_code": "class Item:\n    def __init__(self, p, q): self.p, self.q = p, q\n    def calc(self): return self.p * self.q\nprint(Item(10, 5).calc())\n",
            "test_cases": [{"input": "", "expected": "50"}],
        },
    },

    "les-real-world-projects-5-intermediate": {
        "title": "Inventory Manager Class",
        "content": """# Inventory Manager Class

## 🎯 Goal
Build a manager that handles a COLLECTION of items.

```python
class Manager:
    def __init__(self):
        self.items = []
        
    def add(self, item):
        self.items.append(item)
    
    def report(self):
        for i in self.items:
            print(f"{i.name}: {i.qty}")
```

## 🏆 Key Takeaways
- Composition: The Manager "has-a" list of Items.
""",
        "questions": [
            {"text": "What is the relationship called when one class uses another class as an attribute?", "options": [
                {"text": "Composition", "correct": True}, {"text": "Inheritance", "correct": False},
                {"text": "Polymorphism", "correct": False}, {"text": "Abstraction", "correct": False}]},
        ],
        "challenge": {
            "title": "Stock Counter",
            "description": "Add two items to Manager. Print the length of `self.items`.",
            "initial_code": "# manager logic\n",
            "solution_code": "class M: \n    def __init__(self): self.items = []\n    def add(self, i): self.items.append(i)\nm = M()\nm.add(1); m.add(2)\nprint(len(m.items))\n",
            "test_cases": [{"input": "", "expected": "2"}],
        },
    },

    "les-real-world-projects-5-pro": {
        "title": "Inventory GUI Intro (Tkinter)",
        "content": """# Inventory GUI Intro (Tkinter)

## 🎯 Goal
Take your inventory manager and put it in a Window!

## 📚 The Library
`tkinter` is Python's built-in toolkit for desktop apps.

```python
import tkinter as tk

root = tk.Tk()
root.title("Inventory System")

label = tk.Label(root, text="Welcome!")
label.pack()

root.mainloop()
```

## 🏆 Key Takeaways
- Even after 30 years, `tkinter` is still great for quick internal tools.
""",
        "questions": [
            {"text": "Which built-in library is most commonly used for simple desktop GUIs in Python?", "options": [
                {"text": "tkinter", "correct": True}, {"text": "pygame", "correct": False},
                {"text": "pandas", "correct": False}, {"text": "math", "correct": False}]},
        ],
        "challenge": {
            "title": "GUI Loop",
            "description": "What is the method called on the root object to start the event loop? Print it.",
            "initial_code": "# method name\n",
            "solution_code": "print('mainloop')\n",
            "test_cases": [{"input": "", "expected": "mainloop"}],
        },
    },
}

class Command(BaseCommand):
    help = "Hydrate Module 10 (Projects) — Lessons 1-5"

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
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Hydrated {count} lessons in Module 10 (1-5)"))
