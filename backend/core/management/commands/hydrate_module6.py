"""python manage.py hydrate_module6 -- Module 6 File Handling Lessons 1-5"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Lesson, Quiz, Question, Challenge

LESSONS = {
    # ── Lesson 1: Reading Files ──────────────────────────────────────────────
    "les-file-handling-1-beginner": {
        "title": "Reading Text Files",
        "content": """# Reading Text Files

## 🎯 Learning Objectives
- Open a file in read mode
- Read the entire content vs reading line-by-line
- Understand why you must close files

## 📚 Concept Overview
To work with a file, you first need to `open()` it. Python provides different modes:
- `'r'`: Read (default)
- `'w'`: Write (overwrites)
- `'a'`: Append

```python
f = open("data.txt", "r")
content = f.read()
print(content)
f.close() # Important!
```

### Reading Methods
- `f.read()`: Reads everything as one string.
- `f.readline()`: Reads the next single line.
- `f.readlines()`: Returns a list of all lines.

## 🏆 Key Takeaways
- Always close a file after you're done with it to free system resources.
- For most cases, reading line-by-line is better for memory.
""",
        "questions": [
            {"text": "What is the default mode when opening a file?", "options": [
                {"text": "read ('r')", "correct": True}, {"text": "write ('w')", "correct": False},
                {"text": "append ('a')", "correct": False}, {"text": "binary ('b')", "correct": False}]},
            {"text": "Which method returns a list containing each line of the file as an element?", "options": [
                {"text": "readlines()", "correct": True}, {"text": "read()", "correct": False},
                {"text": "readline()", "correct": False}, {"text": "list()", "correct": False}]},
            {"text": "Why is it important to call file.close()?", "options": [
                {"text": "To release system resources and ensure data is saved", "correct": True},
                {"text": "To delete the file", "correct": False},
                {"text": "To encrypt the file", "correct": False},
                {"text": "It is not important in Python 3", "correct": False}]},
        ],
        "challenge": {
            "title": "Line Counter",
            "description": "Assume a file `input.txt` exists. Store the result of `f.readlines()` in a variable and print the number of lines (length of the list).",
            "initial_code": "# Assume file object 'f' is already open\n",
            "solution_code": "lines = f.readlines()\nprint(len(lines))\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-file-handling-1-intermediate": {
        "title": "Safe Reading & Encoding",
        "content": """# Safe Reading & Encoding

## 🎯 Learning Objectives
- Handle non-ASCII characters with `encoding`
- Check if a file exists before opening
- Understand the difference between text and binary mode

## 📚 Concept Overview
### Encoding
Different systems use different text encodings (UTF-8, UTF-16, etc.). It's a best practice to specify it.
```python
f = open("data.txt", "r", encoding="utf-8")
```

### Modes Recap
- `'rt'`: Read Text (default)
- `'rb'`: Read Binary (for images, pdfs)

## 🏆 Key Takeaways
- Always use `encoding="utf-8"` when working with text to avoid "UnicodeDecodeError".
""",
        "questions": [
            {"text": "Which parameter should you specify to handle emojis or international characters in a text file?", "options": [
                {"text": "encoding='utf-8'", "correct": True}, {"text": "mode='emoji'", "correct": False},
                {"text": "binary=True", "correct": False}, {"text": "type='text'", "correct": False}]},
        ],
        "challenge": {
            "title": "UTF-8 Opener",
            "description": "Write the line of code to open 'notes.txt' for reading with UTF-8 encoding. Store it in variable `my_file`.",
            "initial_code": "# Open with specific encoding\n",
            "solution_code": "my_file = open('notes.txt', 'r', encoding='utf-8')\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-file-handling-1-pro": {
        "title": "Memory Efficient Reading (Chunking)",
        "content": """# Memory Efficient Reading (Chunking)

## 🎯 Learning Objectives
- Read massive files without crashing the machine
- Use the `read(size)` method to process chunks
- Iterate over the file object directly (the preferred way)

## 📚 Concept Overview
Reading a 10GB file with `.read()` will crash a standard computer because it tries to load everything into RAM.

### The Correct Way
File objects are **iterators**. You can loop over them directly to process one line at a time.
```python
with open("big_data.txt") as f:
    for line in f:
        process(line) # Only one line in memory at once!
```

### Chunking
```python
while True:
    chunk = f.read(1024) # 1KB at a time
    if not chunk: break
```

## ️🏆 Key Takeaways
- Never use `.read()` on files of unknown size.
- Use `for line in f:` as your default way to read files.
""",
        "questions": [
            {"text": "Which of these is the most memory-efficient way to process a huge file?", "options": [
                {"text": "for line in f:", "correct": True}, {"text": "f.read()", "correct": False},
                {"text": "f.readlines()", "correct": False}, {"text": "list(f)", "correct": False}]},
        ],
        "challenge": {
            "title": "Chunk Processor",
            "description": "You need to count how many 'A' characters are in a huge file. Write a loop using `.read(100)` to update a `count` variable.",
            "initial_code": "count = 0\n# Loop with chunks of 100\n",
            "solution_code": "while True:\n    chunk = f.read(100)\n    if not chunk: break\n    count += chunk.count('A')\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    # ── Lesson 2: Writing & Appending ────────────────────────────────────────
    "les-file-handling-2-beginner": {
        "title": "Writing to Files",
        "content": """# Writing to Files

## 🎯 Learning Objectives
- Create new files using `'w'` mode
- Append to existing files using `'a'` mode
- Understand that `'w'` overwrites everything!

## 📚 Concept Overview
### Writing ('w')
If the file doesn't exist, it is created. If it DOES exist, its previous content is deleted!
```python
f = open("hello.txt", "w")
f.write("Hello World\\n")
f.close()
```

### Appending ('a')
Adds content to the end of the file.
```python
f = open("hello.txt", "a")
f.write("New line!\\n")
f.close()
```

## 🏆 Key Takeaways
- Be careful with `'w'` mode to avoid accidental data loss.
- `write()` does not add a newline automatically; you must include `\\n`.
""",
        "questions": [
            {"text": "What happens if you open a file in 'w' mode and it already has content?", "options": [
                {"text": "All existing content is deleted (overwritten)", "correct": True},
                {"text": "New content is added to the end", "correct": False},
                {"text": "Python raises an error", "correct": False},
                {"text": "A duplicate file is created", "correct": False}]},
            {"text": "Which mode should you use to add text to the end of a log file without deleting it?", "options": [
                {"text": "append ('a')", "correct": True}, {"text": "write ('w')", "correct": False},
                {"text": "read ('r')", "correct": False}, {"text": "create ('x')", "correct": False}]},
        ],
        "challenge": {
            "title": "Logger Sim",
            "description": "Read a message from the user. Open 'log.txt' in append mode and write the message followed by a newline.",
            "initial_code": "msg = input()\n# Append to file\n",
            "solution_code": "f = open('log.txt', 'a')\nf.write(msg + '\\n')\nf.close()\n",
            "test_cases": [{"input": "Error happened", "expected": ""}],
        },
    },

    "les-file-handling-2-intermediate": {
        "title": "Writing Multiple Lines",
        "content": """# Writing Multiple Lines

## 🎯 Learning Objectives
- Use `writelines()` with a list of strings
- Handle line endings manually
- Flush the buffer

## 📚 Concept Overview
```python
lines = ["First Line\\n", "Second Line\\n"]
f = open("data.txt", "w")
f.writelines(lines)
f.close()
```

### Buffering
Python doesn't always write to the disk immediately for speed. It waits until a buffer is full. `f.close()` or `f.flush()` forces the write to happen.

## 🏆 Key Takeaways
- `writelines` takes a list but doesn't add newlines for you.
- Always use `\\n` to separate lines in your strings.
""",
        "questions": [
            {"text": "Does `writelines(['A', 'B'])` add a newline between 'A' and 'B'?", "options": [
                {"text": "No", "correct": True}, {"text": "Yes", "correct": False},
                {"text": "Only in version 3.8+", "correct": False}, {"text": "Only if using windows", "correct": False}]},
        ],
        "challenge": {
            "title": "List Saver",
            "description": "Take a list `L = ['item1', 'item2']`. Write them to 'out.txt' such that each is on a new line.",
            "initial_code": "L = ['item1', 'item2']\n# Use a loop or writelines with joins\n",
            "solution_code": "f = open('out.txt', 'w')\nf.writelines([f'{x}\\n' for x in L])\nf.close()\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-file-handling-2-pro": {
        "title": "Exclusive Creation ('x' mode)",
        "content": """# Exclusive Creation ('x' mode)

## 🎯 Learning Objectives
- Prevent overwriting by using `'x'` mode
- Understand file system race conditions
- Use `tell()` and `seek()` to navigate the file pointer

## 📚 Concept Overview
### Exclusive mode
If you use `'x'`, the `open` call will FAIL with a `FileExistsError` if the file already exists.
```python
try:
    f = open("data.txt", "x")
except FileExistsError:
    print("Safe! I didn't overwrite your work.")
```

### The File Pointer
- `f.tell()`: Where is the "cursor" now?
- `f.seek(offset)`: Move the "cursor" to a specific byte.

## 🏆 Key Takeaways
- Use `'x'` for safety in mission-critical apps.
- `seek(0)` is a common way to "rewind" to the start of a file.
""",
        "questions": [
            {"text": "Which mode fails if the file already exists?", "options": [
                {"text": "x", "correct": True}, {"text": "w", "correct": False},
                {"text": "a", "correct": False}, {"text": "r", "correct": False}]},
            {"text": "How do you move the file read/write pointer back to the beginning of the file?", "options": [
                {"text": "f.seek(0)", "correct": True}, {"text": "f.rewind()", "correct": False},
                {"text": "f.reset()", "correct": False}, {"text": "f.tell(0)", "correct": False}]},
        ],
        "challenge": {
            "title": "Rewind Master",
            "description": "Assume `f` is open. You just read to the end. Write the line of code to move the pointer back to the 10th byte of the file.",
            "initial_code": "# Use seek\n",
            "solution_code": "f.seek(10)\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    # ── Lesson 3: The with statement (Context Managers) ───────────────────────
    "les-file-handling-3-beginner": {
        "title": "The 'With' Statement",
        "content": """# The 'With' Statement

## 🎯 Learning Objectives
- Use Context Managers for safer file handling
- Understand why `with` is preferred over `close()`
- Automatically handle errors and closing

## 📚 Concept Overview
The `with` statement ensures that the file is **automatically closed**, even if an error occurs inside the block.

```python
with open("data.txt", "w") as f:
    f.write("Safe and sound!")

# No need to call f.close() here. It's already done!
```

## ️🏆 Key Takeaways
- **Rule of thumb**: Always use `with` when opening files in Python.
- It prevents memory leaks and file corruption.
""",
        "questions": [
            {"text": "What is the primary benefit of using the `with` statement?", "options": [
                {"text": "It automatically closes the file for you", "correct": True},
                {"text": "It makes the code run faster", "correct": False},
                {"text": "It compresses the file", "correct": False},
                {"text": "It allows you to open two files at once", "correct": False}]},
            {"text": "What happens if an error occurs inside a `with` block?", "options": [
                {"text": "The file is still closed automatically", "correct": True},
                {"text": "The file remains open until the OS reboots", "correct": False},
                {"text": "The file is deleted", "correct": False},
                {"text": "Python hangs indefinitely", "correct": False}]},
        ],
        "challenge": {
            "title": "Modern Writer",
            "description": "Rewrite the following using a `with` block: `f = open('out.txt', 'w'); f.write('hi'); f.close()`",
            "initial_code": "# Use 'with'\n",
            "solution_code": "with open('out.txt', 'w') as f:\n    f.write('hi')\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-file-handling-3-intermediate": {
        "title": "Working with Multiple Files",
        "content": """# Working with Multiple Files

## 🎯 Learning Objectives
- Open two files in a single `with` statement
- Copy data from one file to another efficiently
- Nest context managers

## 📚 Concept Overview
You can manage multiple resources together.
```python
with open("source.txt", "r") as f_in, open("target.txt", "w") as f_out:
    content = f_in.read()
    f_out.write(content)
```

## 🏆 Key Takeaways
- Keep your logic clean by managing all resources in one `with` block if they are related.
""",
        "questions": [
            {"text": "Can you open two files in a single `with` statement?", "options": [
                {"text": "Yes, using a comma", "correct": True}, {"text": "No", "correct": False},
                {"text": "Only in Python 3.12+", "correct": False}, {"text": "Only for reading", "correct": False}]},
        ],
        "challenge": {
            "title": "File Copier",
            "description": "Open `a.txt` for reading and `b.txt` for writing. For each line in `a`, write it into `b`.",
            "initial_code": "# Use with for both\n",
            "solution_code": "with open('a.txt', 'r') as fr, open('b.txt', 'w') as fw:\n    for line in fr:\n        fw.write(line)\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-file-handling-3-pro": {
        "title": "Custom Context Managers",
        "content": """# Custom Context Managers

## 🎯 Learning Objectives
- Understand the `__enter__` and `__exit__` methods
- Create your own resource handlers
- Use `contextlib` for easier managers

## 📚 Concept Overview
You can make any class work with `with` by implementing two "Dunder" methods.

```python
class MyFile:
    def __enter__(self):
        # Setup stuff
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup stuff
        pass
```

### @contextmanager
```python
from contextlib import contextmanager

@contextmanager
def simple_manager():
    print("Setup")
    yield
    print("Cleanup")
```

## 🏆 Key Takeaways
- Context managers are for more than just files (Database connections, Network sockets, GUI locks).
""",
        "questions": [
            {"text": "Which method is called at the END of a `with` block?", "options": [
                {"text": "__exit__", "correct": True}, {"text": "__end__", "correct": False},
                {"text": "__close__", "correct": False}, {"text": "__stop__", "correct": False}]},
        ],
        "challenge": {
            "title": "Timer Manager",
            "description": "Create a placeholder context manager using `@contextmanager` that prints 'START' before and 'END' after the yield.",
            "initial_code": "from contextlib import contextmanager\n# Define the manager\n",
            "solution_code": "from contextlib import contextmanager\n@contextmanager\ndef timer():\n    print('START')\n    yield\n    print('END')\nwith timer():\n    pass\n",
            "test_cases": [{"input": "", "expected": "START\nEND"}],
        },
    },

    # ── Lesson 4: Working with File Paths ────────────────────────────────────
    "les-file-handling-4-beginner": {
        "title": "Directories & OS module",
        "content": """# Directories & OS module

## 🎯 Learning Objectives
- List files in a directory
- Check if a file or folder exists
- Create and remove directories

## 📚 Concept Overview
The `os` module carries all the fundamental tools for talking to your hard drive.

```python
import os

# Check if exists
if os.path.exists("data/"):
    print("Found it!")

# List content
print(os.listdir("."))

# Make/Remove
os.mkdir("new_folder")
os.rmdir("new_folder") # Only works if empty!
```

## 🏆 Key Takeaways
- Use `os.path.exists()` before opening a file to avoid errors.
- Paths can be **Relative** (starting from your script) or **Absolute** (starting from C: or /).
""",
        "questions": [
            {"text": "Which function check if a file exists on disk?", "options": [
                {"text": "os.path.exists()", "correct": True}, {"text": "os.check()", "correct": False},
                {"text": "file.is_real()", "correct": False}, {"text": "sys.path.has()", "correct": False}]},
            {"text": "What does `os.listdir('.')` do?", "options": [
                {"text": "Lists files in the current directory", "correct": True},
                {"text": "Deletes the directory", "correct": False},
                {"text": "Creates a hidden file", "correct": False},
                {"text": "Lists all users on the OS", "correct": False}]},
        ],
        "challenge": {
            "title": "Folder Creator",
            "description": "Import `os`. Read a folder name from the user. If it does NOT exist, create it.",
            "initial_code": "import os\n# Check and create\n",
            "solution_code": "import os\nname = input().strip()\nif not os.path.exists(name):\n    os.mkdir(name)\n",
            "test_cases": [{"input": "test_dir", "expected": ""}],
        },
    },

    "les-file-handling-4-intermediate": {
        "title": "Pathlib — Modern Path Handling",
        "content": """# Pathlib — Modern Path Handling

## 🎯 Learning Objectives
- Use the `Path` object instead of strings
- Join paths safely across Windows and Linux
- Read/Write files in one line with pathlib

## 📚 Concept Overview
`pathlib` is the modern, readable way to handle file paths. It treats paths as **objects**, not just strings.

```python
from pathlib import Path

# Create a path object
p = Path("data") / "users" / "config.json"
# Note the / operator! It handles slashes correctly on all OS.

if p.exists():
    content = p.read_text() # Open, Read, Close in one go!
```

## 🏆 Key Takeaways
- `pathlib` is cleaner and safer than the old `os.path`.
- The `/` operator makes combining paths intuitive.
""",
        "questions": [
            {"text": "Which module is the modern, object-oriented alternative to `os.path`?", "options": [
                {"text": "pathlib", "correct": True}, {"text": "path", "correct": False},
                {"text": "filepath", "correct": False}, {"text": "syspath", "correct": False}]},
            {"text": "In `pathlib`, how do you join two path parts?", "options": [
                {"text": "Using the / operator", "correct": True}, {"text": "Using +", "correct": False},
                {"text": "Using .join()", "correct": False}, {"text": "Using &", "correct": False}]},
        ],
        "challenge": {
            "title": "Path Explorer",
            "description": "Using `pathlib.Path`, check if a file 'test.py' exists and print its file size (stat.st_size).",
            "initial_code": "from pathlib import Path\n# Use Path objects\n",
            "solution_code": "from pathlib import Path\np = Path('test.py')\nif p.exists():\n    print(p.stat().st_size)\n",
            "test_cases": [{"input": "", "expected": "*"}],
        },
    },

    "les-file-handling-4-pro": {
        "title": "Globbing and Recursive Search",
        "content": """# Globbing and Recursive Search

## 🎯 Learning Objectives
- Search for files using patterns (e.g., `*.py`)
- Walk through entire folder trees effortlessly
- Filter files by extension or name

## 📚 Concept Overview
"Globbing" is the name for pattern-based file searching.

```python
from pathlib import Path

# Find all python files in current folder
for p in Path('.').glob('*.py'):
    print(p.name)

# Find all python files including sub-folders
for p in Path('.').rglob('*.py'):
    print(p)
```

## 🏆 Key Takeaways
- `glob` searches current level.
- `rglob` (recursive glob) searches everything inside.
""",
        "questions": [
            {"text": "Which method in `pathlib` finds files in subdirectories too?", "options": [
                {"text": "rglob()", "correct": True}, {"text": "glob()", "correct": False},
                {"text": "findall()", "correct": False}, {"text": "search()", "correct": False}]},
        ],
        "challenge": {
            "title": "Txt Finder",
            "description": "Using `pathlib.Path`, print the name of every `.txt` file found recursively in the current directory.",
            "initial_code": "from pathlib import Path\n# Use rglob\n",
            "solution_code": "from pathlib import Path\nfor p in Path('.').rglob('*.txt'):\n    print(p.name)\n",
            "test_cases": [{"input": "", "expected": "*"}],
        },
    },

    # ── Lesson 5: Standard Text Formats (CSV Basics) ─────────────────────────
    "les-file-handling-5-beginner": {
        "title": "Reading & Writing CSV",
        "content": """# Reading & Writing CSV

## 🎯 Learning Objectives
- Understand the CSV format (Comma Separated Values)
- Use the built-in `csv` module
- Handle rows as lists

## 📚 Concept Overview
A CSV is basically a spreadsheet in text form.

```python
import csv

# Reading
with open("data.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row) # row is a list of strings

# Writing
with open("out.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Age"])
    writer.writerow(["Alice", "25"])
```

## ⚠️ Common Pitfalls
- Forgetting `newline=""` in Windows leads to extra blank lines in your CSV.
- Assuming CSVs always use commas (they can use tabs, semicolons, etc.).

## 🏆 Key Takeaways
- `csv.reader` makes it much safer than using `split(',')` manually.
""",
        "questions": [
            {"text": "What does CSV stand for?", "options": [
                {"text": "Comma Separated Values", "correct": True}, {"text": "Column Sorted Variables", "correct": False},
                {"text": "Code Set Verification", "correct": False}, {"text": "Common Sheet View", "correct": False}]},
            {"text": "Why should you use the `csv` module instead of `split(',')`?", "options": [
                {"text": "It handles data containing commas (e.g., 'London, UK') correctly within quotes", "correct": True},
                {"text": "It is faster for integers", "correct": False},
                {"text": "It encrypts the data", "correct": False},
                {"text": "It only works with excel", "correct": False}]},
        ],
        "challenge": {
            "title": "CSV Row Counter",
            "description": "Read 'data.csv'. Print the total number of rows (excluding a header if you want, but just count total for now).",
            "initial_code": "import csv\n# Count rows\n",
            "solution_code": "import csv\nwith open('data.csv', 'r') as f:\n    print(len(list(csv.reader(f))))\n",
            "test_cases": [{"input": "", "expected": "*"}],
        },
    },

    "les-file-handling-5-intermediate": {
        "title": "DictReader & DictWriter",
        "content": """# DictReader & DictWriter

## 🎯 Learning Objectives
- Read CSV rows as dictionaries
- Write items by key name
- Improve code readability for large datasets

## 📚 Concept Overview
Using dictionaries is much safer than remembering that "Age" is index `[1]`.

```python
import csv

with open("data.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["Name"], row["Age"])
```

## 🏆 Key Takeaways
- `DictReader` automatically uses the first line of the file as keys.
""",
        "questions": [
            {"text": "Which class reads CSV rows directly into a dictionary?", "options": [
                {"text": "csv.DictReader", "correct": True}, {"text": "csv.MapReader", "correct": False},
                {"text": "csv.JsonReader", "correct": False}, {"text": "csv.reader(dict=True)", "correct": False}]},
        ],
        "challenge": {
            "title": "Header Extraction",
            "description": "Open 'data.csv' with `DictReader`. Print the list of field names (headers).",
            "initial_code": "import csv\n# Print headers\n",
            "solution_code": "import csv\nwith open('data.csv', 'r') as f:\n    r = csv.DictReader(f)\n    print(r.fieldnames)\n",
            "test_cases": [{"input": "", "expected": "*"}],
        },
    },

    "les-file-handling-5-pro": {
        "title": "Custom Delimiters & Dialects",
        "content": """# Custom Delimiters & Dialects

## 🎯 Learning Objectives
- Read files that use `|` or `\\t` (TSV)
- Handle quotes and escape characters
- Understand CSV "Dialects" (Excel, Unix, etc.)

## 📚 Concept Overview
```python
import csv
with open("data.psv", "r") as f:
    # Use | as separator
    reader = csv.reader(f, delimiter="|")
```

If you have a very weird file format, you can register a "Dialect" to reusable formatting rules.

## 🏆 Key Takeaways
- The `delimiter` parameter is key for non-standard CSV files.
""",
        "questions": [
            {"text": "Which parameter allows you to change the separator character in `csv.reader`?", "options": [
                {"text": "delimiter", "correct": True}, {"text": "separator", "correct": False},
                {"text": "split_char", "correct": False}, {"text": "marker", "correct": False}]},
        ],
        "challenge": {
            "title": "TSV Reader",
            "description": "Write the code to create a `csv.reader` for a file `f` that uses tabs (`\\t`) as delimiters.",
            "initial_code": "import csv\n# Set delimiter\n",
            "solution_code": "reader = csv.reader(f, delimiter='\\t')\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },
}

class Command(BaseCommand):
    help = "Hydrate Module 6 (File Handling) — Lessons 1-5"

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
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Hydrated {count} lessons in Module 6 (1-5)"))
