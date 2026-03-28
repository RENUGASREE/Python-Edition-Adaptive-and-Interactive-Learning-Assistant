"""python manage.py hydrate_module6_b -- Module 6 File Handling Lessons 6-10"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Lesson, Quiz, Question, Challenge

LESSONS = {
    # ── Lesson 6: JSON Files ─────────────────────────────────────────────────
    "les-file-handling-6-beginner": {
        "title": "Working with JSON",
        "content": """# Working with JSON

## 🎯 Learning Objectives
- Understand the JSON (JavaScript Object Notation) format
- Use the `json` module to read and write files
- Map JSON data to Python dictionaries and lists

## 📚 Concept Overview
JSON is the most common format for exchanging data on the internet. It looks almost identical to Python dictionaries and lists.

### Reading JSON File
```python
import json

with open("config.json", "r") as f:
    data = json.load(f) # Returns a dict
    print(data["version"])
```

### Writing JSON File
```python
user = {"id": 1, "name": "Alice"}
with open("user.json", "w") as f:
    json.dump(user, f, indent=4) # indent makes it readable!
```

## 🏆 Key Takeaways
- Use `json.load()` for files and `json.loads()` for strings.
- Use `json.dump()` for files and `json.dumps()` for strings.
- Indentation makes the file human-readable but increases the file size slightly.
""",
        "questions": [
            {"text": "Which module allows you to work with JSON in Python?", "options": [
                {"text": "json", "correct": True}, {"text": "dict", "correct": False},
                {"text": "serial", "correct": False}, {"text": "web", "correct": False}]},
            {"text": "What is the difference between `json.load()` and `json.loads()`?", "options": [
                {"text": "load() reads from a file; loads() reads from a string", "correct": True},
                {"text": "loads() is faster", "correct": False},
                {"text": "load() is only for lists", "correct": False},
                {"text": "There is no difference", "correct": False}]},
        ],
        "challenge": {
            "title": "JSON Extractor",
            "description": "Assume `f` is an open file object for `settings.json`. Write the line of code to parse it into a variable named `settings`.",
            "initial_code": "import json\n# Parse file f\n",
            "solution_code": "import json\nsettings = json.load(f)\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-file-handling-6-intermediate": {
        "title": "Encoding Custom Objects in JSON",
        "content": """# Encoding Custom Objects in JSON

## 🎯 Learning Objectives
- Handle "Object of type X is not JSON serializable" errors
- Create custom JSON encoders
- Use the `default` parameter in `json.dump()`

## 📚 Concept Overview
By default, JSON only knows about types like `int`, `str`, `list`, `dict`, and `None`. If you try to save a custom class or a `datetime` object, it fails.

### Solution: The Default function
```python
import json
from datetime import datetime

def date_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

data = {"time": datetime.now()}
print(json.dumps(data, default=date_serializer))
```

## 🏆 Key Takeaways
- Use a custom serializer function to handle dates and other complex objects.
- `isoformat()` is the best way to represent dates in JSON.
""",
        "questions": [
            {"text": "Which parameter in `json.dumps` allows you to specify a function to handle non-standard types?", "options": [
                {"text": "default", "correct": True}, {"text": "fallback", "correct": False},
                {"text": "custom", "correct": False}, {"text": "error", "correct": False}]},
        ],
        "challenge": {
            "title": "Custom Serializer",
            "description": "Write a function `ser(obj)` that returns the string 'PLACEHOLDER' if the object is NOT a standard JSON type. Use it in `json.dumps(my_data, default=ser)`.",
            "initial_code": "def ser(obj):\n    # Return 'PLACEHOLDER' if not basic type\n",
            "solution_code": "def ser(obj):\n    return 'PLACEHOLDER'\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-file-handling-6-pro": {
        "title": "JSON vs Pickle vs Orjson",
        "content": """# JSON vs Pickle vs Orjson

## 🎯 Learning Objectives
- Compare serialization formats
- Understand performance bottlenecks in standard `json`
- Introduction to `orjson` and `ujson` for high-throughput apps

## 📚 Concept Overview
| Format | Speed | Safety | Language Support |
|--------|-------|--------|------------------|
| **JSON** | Medium | High | Universal |
| **Pickle** | Fast | Low | Python Only |
| **orjson** | Extreme| High | Universal |

`orjson` is a fast alternative for JSON that handles `datetime` and `numpy` objects natively. It's used in high-performance web servers like FastAPI.

## 🏆 Key Takeaways
- Standard `json` is fine for most apps.
- Use `orjson` if you are processing millions of JSON objects per second.
""",
        "questions": [
            {"text": "Which format is Python-only and can execute arbitrary code?", "options": [
                {"text": "Pickle", "correct": True}, {"text": "JSON", "correct": False},
                {"text": "XML", "correct": False}, {"text": "YAML", "correct": False}]},
        ],
        "challenge": {
            "title": "Format Choice",
            "description": "You need to send data from a Python backend to a React frontend. Which format should you use? Print 'JSON' or 'Pickle'.",
            "initial_code": "# Best for web\n",
            "solution_code": "print('JSON')\n",
            "test_cases": [{"input": "", "expected": "JSON"}],
        },
    },

    # ── Lesson 7: Binary Files & Images ──────────────────────────────────────
    "les-file-handling-7-beginner": {
        "title": "Binary Mode Basics",
        "content": """# Binary Mode Basics

## 🎯 Learning Objectives
- Understand the difference between text (`'t'`) and binary (`'b'`) modes
- Open non-text files (images, sounds, etc.)
- Use the `bytes` type

## 📚 Concept Overview
Text files handle strings. Binary files handle raw bytes. If you open an image as text, it will give you a "UnicodeDecodeError".

```python
# Open image for reading
with open("photo.jpg", "rb") as f:
    data = f.read(10) # Read the first 10 bytes
    print(len(data)) # Check length
```

### Bytes Literal
Byte objects start with a `b` prefix: `b"Hello"`.

## 🏆 Key Takeaways
- Use `'rb'` and `'wb'` for anything that isn't a plain text file.
- Binary data is made of integers from 0 to 255 (bytes).
""",
        "questions": [
            {"text": "What mode character represents 'binary'?", "options": [
                {"text": "b", "correct": True}, {"text": "t", "correct": False},
                {"text": "x", "correct": False}, {"text": "a", "correct": False}]},
            {"text": "What does a `b` prefix before a string mean? (e.g. b'test')", "options": [
                {"text": "It is a bytes object, not a string", "correct": True},
                {"text": "It is bold text", "correct": False},
                {"text": "It is a big integer", "correct": False},
                {"text": "It is base64 encoded", "correct": False}]},
        ],
        "challenge": {
            "title": "Byte Writer",
            "description": "Open a file 'secret.bin' for writing in binary mode. Write the bytes `b'abc'` to it.",
            "initial_code": "# Use wb mode\n",
            "solution_code": "with open('secret.bin', 'wb') as f:\n    f.write(b'abc')\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-file-handling-7-intermediate": {
        "title": "Copying Binary Files",
        "content": """# Copying Binary Files

## 🎯 Learning Objectives
- Build a generic file copy tool
- Avoid loading whole binary files into memory
- Verify file copies

## 📚 Concept Overview
```python
def copy_binary(src, dst):
    with open(src, "rb") as f_src, open(dst, "wb") as f_dst:
        while True:
            chunk = f_src.read(4096) # 4KB chunks
            if not chunk: break
            f_dst.write(chunk)
```

## ️🏆 Key Takeaways
- Always use chunks for binary files; you never know how big they are.
- This pattern works for any file type (video, zip, exe).
""",
        "questions": [
            {"text": "Why do we read binary files in chunks?", "options": [
                {"text": "To prevent high memory usage on large files", "correct": True},
                {"text": "To make the file smaller", "correct": False},
                {"text": "To avoid copyright issues", "correct": False},
                {"text": "To encrypt it", "correct": False}]},
        ],
        "challenge": {
            "title": "Buffer Choice",
            "description": "You are copying a 2GB movie. If you use `read()` (no arguments), how much RAM will your program try to use? Print result in GB.",
            "initial_code": "# Memory estimate\n",
            "solution_code": "print('2GB')\n",
            "test_cases": [{"input": "", "expected": "2GB"}],
        },
    },

    "les-file-handling-7-pro": {
        "title": "Struct & Binary Parsing",
        "content": """# Struct & Binary Parsing

## 🎯 Learning Objectives
- Use the `struct` module to parse C-style binary data
- Convert between bytes and Python integers/floats
- Understand Little Endian vs Big Endian

## 📚 Concept Overview
Many file formats save data as packed bytes (e.g., 4 bytes for an integer).

```python
import struct

# Pack an integer into 4 bytes (Little Endian)
data = struct.pack("<I", 1024) 

# Unpack
val = struct.unpack("<I", data) # (1024,)
```

## 🏆 Key Takeaways
- Use `struct` when you need to talk to low-level systems or binary network protocols.
""",
        "questions": [
            {"text": "Which module helps convert Python values to C-style bytes and back?", "options": [
                {"text": "struct", "correct": True}, {"text": "binary", "correct": False},
                {"text": "c_types", "correct": False}, {"text": "protocol", "correct": False}]},
        ],
        "challenge": {
            "title": "Int to Bytes",
            "description": "Use `struct.pack` with format '>I' (Big Endian 4-byte int) to pack the number 1. Print the length of the resulting bytes object.",
            "initial_code": "import struct\n# Pack 1\n",
            "solution_code": "import struct\nprint(len(struct.pack('>I', 1)))\n",
            "test_cases": [{"input": "", "expected": "4"}],
        },
    },

    # ── Lesson 8: Advanced OS operations ─────────────────────────────────────
    "les-file-handling-8-beginner": {
        "title": "Renaming & Deleting",
        "content": """# Renaming & Deleting

## 🎯 Learning Objectives
- Use `os.rename()` and `os.remove()`
- Handle common errors (File Not Found)
- Use `shutil` for moving files

## 📚 Concept Overview
```python
import os
import shutil

# Basic Rename/Move
os.rename("old.txt", "new.txt")

# Delete file
os.remove("junk.txt")

# Delete entire folder (Careful!)
shutil.rmtree("temp_dir")

# Check stats
info = os.stat("data.txt")
print(f"Size: {info.st_size} bytes")
```

## 🏆 Key Takeaways
- `os.remove` is for files; `os.rmdir` is for empty folders.
- `shutil` provides high-level operations like copying and recursive deletion.
""",
        "questions": [
            {"text": "Which function deletes a single file?", "options": [
                {"text": "os.remove()", "correct": True}, {"text": "os.delete()", "correct": False},
                {"text": "os.rmdir()", "correct": False}, {"text": "shutil.erase()", "correct": False}]},
            {"text": "Which module is best for copying an entire directory?", "options": [
                {"text": "shutil", "correct": True}, {"text": "os", "correct": False},
                {"text": "sys", "correct": False}, {"text": "pathlib", "correct": False}]},
        ],
        "challenge": {
            "title": "Safety Move",
            "description": "Write a check: If 'a.txt' exists, rename it to 'b.txt', otherwise print 'Skip'.",
            "initial_code": "import os\n# Rename safely\n",
            "solution_code": "import os\nif os.path.exists('a.txt'):\n    os.rename('a.txt', 'b.txt')\nelse:\n    print('Skip')\n",
            "test_cases": [{"input": "", "expected": "Skip"}],
        },
    },

    "les-file-handling-8-intermediate": {
        "title": "Temporary Files & Folders",
        "content": """# Temporary Files & Folders

## 🎯 Learning Objectives
- Use the `tempfile` module
- Create files that are automatically deleted
- Handle scratch data securely

## 📚 Concept Overview
Creating scratch files manually can leave junk on the user's disk if your program crashes. `tempfile` handles this correctly.

```python
import tempfile

with tempfile.NamedTemporaryFile(delete=True) as temp:
    print(f"I created {temp.name}")
    temp.write(b"Scratch data")
# File is deleted automatically after the 'with' block!
```

## 🏆 Key Takeaways
- `tempfile` is the only safe way to handle temporary data.
- It automatically picks the correct Temp folder for the OS (Windows, Linux, etc.).
""",
        "questions": [
            {"text": "What is the main advantage of the `tempfile` module?", "options": [
                {"text": "It automatically cleans up the generated files", "correct": True},
                {"text": "It makes files faster", "correct": False},
                {"text": "It hides the files from the user", "correct": False},
                {"text": "It compresses the files", "correct": False}]},
        ],
        "challenge": {
            "title": "Temp Namer",
            "description": "Import `tempfile`. Use `tempfile.gettempdir()` to print the path to the system's temporary directory.",
            "initial_code": "import tempfile\n# Get temp dir path\n",
            "solution_code": "import tempfile\nprint(tempfile.gettempdir())\n",
            "test_cases": [{"input": "", "expected": "*"}],
        },
    },

    "les-file-handling-8-pro": {
        "title": "File Locks & Permissions",
        "content": """# File Locks & Permissions

## 🎯 Learning Objectives
- Handle "Permission Denied" errors
- Use `os.chmod` to change file security
- Understand file locking for multi-process apps

## 📚 Concept Overview
Sometimes a file is "In Use" or "Read Only".

```python
import os
import stat

# Make read-only
os.chmod("file.txt", stat.S_IREAD)

# Make writeable again
os.chmod("file.txt", stat.S_IWRITE)
```

### Locking
Python doesn't have a reliable built-in file lock for all platforms (Windows vs Unix handled differently). Use external libraries like `portalocker` if you need to prevent two instances of your app from writing to the same file.

## 🏆 Key Takeaways
- Permission errors are common; always use `try/except` around file operations.
- `os.chmod` behaves differently on Windows vs Linux.
""",
        "questions": [
            {"text": "Which exception is raised when you try to write to a read-only file?", "options": [
                {"text": "PermissionError", "correct": True}, {"text": "ValueError", "correct": False},
                {"text": "LockedError", "correct": False}, {"text": "OSLimitError", "correct": False}]},
        ],
        "challenge": {
            "title": "Access Try",
            "description": "Write a `try/except` block that tries to `os.remove('locked.txt')`. If it fails with `PermissionError`, print 'Locked'.",
            "initial_code": "import os\n# Try to delete\n",
            "solution_code": "import os\ntry:\n    os.remove('locked.txt')\nexcept PermissionError:\n    print('Locked')\nexcept FileNotFoundError:\n    pass\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    # ── Lesson 9: Buffering & Streaming ──────────────────────────────────────
    "les-file-handling-9-beginner": {
        "title": "Internal Buffering",
        "content": """# Internal Buffering

## 🎯 Learning Objectives
- Understand how `flush()` works
- Learn about the buffer size in `open()`
- Ensure data is physically on the disk

## 📚 Concept Overview
When you `f.write()`, Python puts the data in a RAM "Buffer" before sending it to the disk.

```python
with open("data.txt", "w") as f:
    f.write("Sent to buffer")
    f.flush() # Force write to disk NOW
    # ... rest of work ...
```

## 🏆 Key Takeaways
- `close()` calls `flush()` automatically.
- Use `flush()` if your program is long-running and you want external apps to see the file updates in real-time.
""",
        "questions": [
            {"text": "What does the `flush()` method do?", "options": [
                {"text": "Forces the text from RAM onto the disk immediately", "correct": True},
                {"text": "Deletes the buffer", "correct": False},
                {"text": "Cleans the hard drive", "correct": False},
                {"text": "Restarts the file pointer", "correct": False}]},
        ],
        "challenge": {
            "title": "Manual Flush",
            "description": "Assume `f` is open. write 'A' and then use the method that ensures it is pushed to the disk without closing the file.",
            "initial_code": "# code line here\n",
            "solution_code": "f.write('A')\nf.flush()\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-file-handling-9-intermediate": {
        "title": "StringIO & BytesIO (Memory Files)",
        "content": """# StringIO & BytesIO (Memory Files)

## 🎯 Learning Objectives
- Treat strings as "Fake Files" in memory
- Speed up testing by avoiding Disk I/O
- Use the `io` module

## 📚 Concept Overview
Sometimes a function requires a "File-like object", but you just want to pass it a string.

```python
from io import StringIO

f = StringIO("Line 1\\nLine 2")
print(f.readline()) # 'Line 1'
```

## 🏆 Key Takeaways
- `StringIO` and `BytesIO` allow you to simulate files without actually using the hard drive.
- This is extremely common in unit testing.
""",
        "questions": [
            {"text": "Which module contains StringIO and BytesIO?", "options": [
                {"text": "io", "correct": True}, {"text": "sys", "correct": False},
                {"text": "string", "correct": False}, {"text": "memory", "correct": False}]},
        ],
        "challenge": {
            "title": "In-Memory Buffer",
            "description": "Use `io.StringIO` to create a fake file from the string 'HELLO'. Use `f.read()` to print its content.",
            "initial_code": "from io import StringIO\n# Fake file\n",
            "solution_code": "from io import StringIO\nf = StringIO('HELLO')\nprint(f.read())\n",
            "test_cases": [{"input": "", "expected": "HELLO"}],
        },
    },

    "les-file-handling-9-pro": {
        "title": "Low-level File Descriptors",
        "content": """# Low-level File Descriptors

## 🎯 Learning Objectives
- Understand how the OS tracks files (integer IDs)
- Distinguish between a File Object and a File Descriptor
- Use `os.open` vs `open`

## 📚 Concept Overview
Standard `open()` is a high-level Python wrapper. In the OS, every open file is just an integer (e.g., 3, 4, 5).

```python
import os
fd = os.open("data.txt", os.O_RDONLY) # Returns integer
content = os.read(fd, 100) # Read 100 bytes
os.close(fd)
```

## ️🏆 Key Takeaways
- Almost always use the high-level `open()`.
- Fileno (descriptors) are useful when talking to other C-libraries via `ctypes`.
""",
        "questions": [
            {"text": "What is a 'File Descriptor' in terms of data type?", "options": [
                {"text": "A non-negative integer", "correct": True}, {"text": "A string", "correct": False},
                {"text": "A boolean", "correct": False}, {"text": "An object in memory", "correct": False}]},
        ],
        "challenge": {
            "title": "Standard FD",
            "description": "In most systems, what is the file descriptor number for 'Standard Output' (stdout)?",
            "initial_code": "# Choice: 0, 1, or 2\n",
            "solution_code": "print(1)\n",
            "test_cases": [{"input": "", "expected": "1"}],
        },
    },

    # ── Lesson 10: Mini Project ──────────────────────────────────────────────
    "les-file-handling-10-beginner": {
        "title": "Project: Log Separator",
        "content": """# Project: Log Separator

## 🎯 Goal
Read a combined log file and separate 'ERROR' lines into a new file.

## 📝 Requirements
- Read `all.log` line by line.
- Check `if "ERROR" in line`.
- Write matches to `errors.log`.
""",
        "questions": [],
        "challenge": {
            "title": "Basic Filter",
            "description": "Read input lines. For each line, if it starts with '!!!', print it. (Simulates log filtering).",
            "initial_code": "# Filter lines\n",
            "solution_code": "import sys\nfor line in sys.stdin:\n    if line.startswith('!!!'):\n        print(line.strip())\n",
            "test_cases": [{"input": "!!! Warning\nInfo\n!!! Error", "expected": "!!! Warning\n!!! Error"}],
        },
    },

    "les-file-handling-10-intermediate": {
        "title": "Project: Config Converter",
        "content": """# Project: Config Converter

## 🎯 Goal
Convert a `.txt` list into a `.json` object.

## 📝 Inputs
`Alice, 25`
`Bob, 30`

## 📝 Outputs
`[{"name": "Alice", "age": 25}, ...]`
""",
        "questions": [],
        "challenge": {
            "title": "Text to JSON",
            "description": "Read one line 'Name, Age'. Split it and print a JSON string of a dictionary representing that person.",
            "initial_code": "import json\n# Convert line to JSON\n",
            "solution_code": "import json\nline = input().split(',')\nname = line[0].strip()\nage = int(line[1].strip())\nprint(json.dumps({'name': name, 'age': age}))\n",
            "test_cases": [{"input": "Bob, 40", "expected": '{"name": "Bob", "age": 40}'}],
        },
    },

    "les-file-handling-10-pro": {
        "title": "Project: File Organizer Script",
        "content": """# Project: File Organizer Script

## 🎯 Goal
Write a script that moves `.jpg` files into an 'Images' folder and `.pdf` files into a 'Docs' folder.

## 📝 Features
- Use `pathlib` for recursive search.
- Create folders if they don't exist.
- Log every move to `history.txt`.
""",
        "questions": [],
        "challenge": {
            "title": "Extension Sorter",
            "description": "Given a list of filenames, print 'IMAGE' if file ends in .jpg, 'DOC' if ends in .pdf, else 'OTHER'.",
            "initial_code": "# Extension logic\n",
            "solution_code": "name = input().lower()\nif name.endswith('.jpg'): print('IMAGE')\nelif name.endswith('.pdf'): print('DOC')\nelse: print('OTHER')\n",
            "test_cases": [{"input": "photo.JPG", "expected": "IMAGE"}, {"input": "resume.pdf", "expected": "DOC"}],
        },
    },
}

class Command(BaseCommand):
    help = "Hydrate Module 6 (File Handling) — Lessons 6-10"

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
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Hydrated {count} lessons in Module 6 (6-10)"))
