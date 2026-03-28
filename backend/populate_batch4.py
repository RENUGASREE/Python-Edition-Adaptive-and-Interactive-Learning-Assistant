import os
import sys
import django

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import Module, Lesson, Challenge

BATCH4_DATA = [
    { "module_id": 21, "topics": [
        { "title": "String Slicing", "beginner": {
            "content": "🟢 BEGINNER LEVEL\n\n📘 Definition\nSlicing is a way to get a part of a string.\n\n🧠 Explanation\nYou use `[start:end]` to pick a range of characters.\n\n🔤 Syntax\ntext[0:5]\n\n📌 Example\ns = 'Python'\nprint(s[0:2]) # Py\n\n🌍 Use Case\nExtracting the 'day' part from a date like 'Monday'.\n\n🧪 Knowledge Check\n1. What does s[1:3] give for 'Hello'?\n\n💻 Challenge\nPrint the first 3 letters of 'Welcome'.",
            "challenge": {
                "title": "Welcome Slice", "description": "Extract first 3 letters from 'Welcome' using slicing.", "initial_code": "s = 'Welcome'\n# Slice", "solution_code": "s = 'Welcome'\nprint(s[0:3])", "test_cases": [{"input": "", "expected": "Wel"}]
            }
        }, "intermediate": {
            "content": "🟡 INTERMEDIATE LEVEL\n\n📘 Definition\nSteps in slicing allow you to skip characters.\n\n🧠 Explanation\n`[start:end:step]` lets you pick every 2nd or 3rd character. Negative step reverses the string.\n\n🔤 Syntax\ntext[::-1]\n\n📌 Example\ns = '12345'\nprint(s[::2]) # 135\n\n🌍 Use Case\nReversing a sequence or picking alternating items from a list.\n\n🧪 Knowledge Check\n1. How to reverse a string?\n\n💻 Challenge\nReverse the string 'Python' using slicing.",
            "challenge": {
                "title": "Reverse Slice", "description": "Reverse 'Python' using `[::-1]`.", "initial_code": "s = 'Python'\n# Rev", "solution_code": "s = 'Python'\nprint(s[::-1])", "test_cases": [{"input": "", "expected": "nohtyP"}]
            }
        }, "pro": {
            "content": "🔴 PRO LEVEL\n\n📘 Definition\nSlice objects and memory views for efficient subsetting.\n\n🧠 Explanation\n`slice(start, end, step)` is a built-in object that can be passed to `[]`.\n\n🔤 Advanced Syntax\nmy_slice = slice(1, 10, 2)\n\n📌 Example\ns = 'abcdefghij'\nprint(s[slice(0, 5)])\n\n🌍 Use Case\nDefining reusable extraction rules for fixed-width data files.\n\n🧪 Knowledge Check\n1. What is the slice() function?\n\n💻 Challenge\nCreate a slice object for every 2nd character and apply it to '0123456789'.",
            "challenge": {
                "title": "Slice Object", "description": "Use `slice(0, 10, 2)` on s='0123456789'.", "initial_code": "s = '0123456789'\n# Use slice()", "solution_code": "s = '0123456789'\nsl = slice(0, 10, 2)\nprint(s[sl])", "test_cases": [{"input": "", "expected": "02468"}]
            }
        } },
        { "title": "Dictionaries", "beginner": {
            "content": "🟢 BEGINNER LEVEL\n\n📘 Definition\nDictionaries store data in 'Key: Value' pairs.\n\n🧠 Explanation\nLike a real dictionary where you look up a word (key) to find its meaning (value).\n\n🔤 Syntax\nd = {'name': 'John'}\n\n📌 Example\ncar = {'brand': 'Ford', 'year': 1964}\nprint(car['brand'])\n\n🌍 Use Case\nStoring user profiles (username, email).\n\n🧪 Knowledge Check\n1. What brackets do dicts use?\n\n💻 Challenge\nCreate a dict with 'city': 'Paris' and print the city.",
            "challenge": {
                "title": "Paris Dict", "description": "Create dict d with key 'city' and value 'Paris'. Print value of 'city'.", "initial_code": "# code", "solution_code": "d = {'city': 'Paris'}\nprint(d['city'])", "test_cases": [{"input": "", "expected": "Paris"}]
            }
        }, "intermediate": {
            "content": "🟡 INTERMEDIATE LEVEL\n\n📘 Definition\nDictionaries are mutable and support methods like `.get()`, `.keys()`, and `.items()`.\n\n🧠 Explanation\n`.get()` is safer because it doesn't crash if the key is missing.\n\n🔤 Syntax\nd.get('key', 'default')\n\n📌 Example\nd = {'a': 1}\nprint(d.get('b', 0)) # 0\n\n🌍 Use Case\nCounting word frequencies in a text document.\n\n🧪 Knowledge Check\n1. Difference between d['key'] and d.get('key')?\n\n💻 Challenge\nUpdate the value of key 'age' from 20 to 21 in dict d.",
            "challenge": {
                "title": "Update Dict", "description": "Update d={'age': 20} to age=21 and print d.", "initial_code": "d = {'age': 20}\n# Update", "solution_code": "d = {'age': 20}\nd['age'] = 21\nprint(d)", "test_cases": [{"input": "", "expected": "{'age': 21}"}]
            }
        }, "pro": {
            "content": "🔴 PRO LEVEL\n\n📘 Definition\nDictionary comprehensions and efficient hashing logic.\n\n🧠 Explanation\nDicts in Python 3.7+ preserve insertion order. Hashing ensures O(1) lookup.\n\n🔤 Advanced Syntax\nsq = {x: x*x for x in range(5)}\n\n📌 Example\nd = {k: v for k, v in zip(['a', 'b'], [1, 2])}\n\n🌍 Use Case\nMapping complex data structures or caching function results (memoization).\n\n🧪 Knowledge Check\n1. What is the time complexity of dict lookup?\n\n💻 Challenge\nCreate a dict of squares for 1 to 5 using dict comprehension.",
            "challenge": {
                "title": "Dict Comp", "description": "Generate {1: 1, 2: 4, 3: 9} etc for 1..3 using comprehension.", "initial_code": "# code", "solution_code": "d = {x: x*x for x in range(1, 4)}\nprint(d)", "test_cases": [{"input": "", "expected": "{1: 1, 2: 4, 3: 9}"}]
            }
        } }
    ] }
]

def populate_batch4():
    print("🚀 Starting Batch 4 Population...")
    total_l = 0; total_c = 0
    for med in BATCH4_DATA:
        mid = med["module_id"]
        for topic in med["topics"]:
            title = topic["title"]
            for level in ["beginner", "intermediate", "pro"]:
                dl = level.capitalize()
                Lesson.objects.filter(module_id=mid, title=title, difficulty=dl).delete()
                l = Lesson.objects.create(module_id=mid, title=title, difficulty=dl, content=topic[level]["content"], slug=title.lower().replace(" ", "-"), order=50, duration=15)
                total_l += 1
                c_data = topic[level]["challenge"]
                Challenge.objects.filter(lesson_id=l.id).delete()
                Challenge.objects.create(lesson_id=l.id, title=c_data["title"], description=c_data["description"], initial_code=c_data["initial_code"], solution_code=c_data["solution_code"], test_cases=c_data["test_cases"], points=100, difficulty=dl)
                total_c += 1
    print(f"✅ Success! Created {total_l} Lessons and {total_c} Challenges.")

if __name__ == "__main__":
    populate_batch4()
