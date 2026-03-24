#!/usr/bin/env python
import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from lessons.models import LessonChunk

# Create sample lesson data
sample_lessons = [
    {
        "lesson_id": 1,
        "topic": "Python Variables",
        "content": "Variables in Python are containers for storing data values. You create a variable by assigning a value to it:\n\n```python\nname = 'John'\nage = 25\nheight = 5.9\n```\n\nPython automatically determines the type of the variable based on the value you assign."
    },
    {
        "lesson_id": 2,
        "topic": "Python Functions",
        "content": "Functions are blocks of reusable code that perform a specific task. You define a function using the 'def' keyword:\n\n```python\ndef greet(name):\n    return f'Hello, {name}!'\n\n# Call the function\nmessage = greet('Alice')\nprint(message)  # Output: Hello, Alice!\n```\n\nFunctions can take parameters and return values."
    },
    {
        "lesson_id": 3,
        "topic": "Python Lists",
        "content": "Lists are ordered collections of items in Python. You can create a list using square brackets:\n\n```python\nfruits = ['apple', 'banana', 'orange']\nnumbers = [1, 2, 3, 4, 5]\n\n# Access items\nprint(fruits[0])  # Output: apple\n\n# Add items\nfruits.append('grape')\n\n# Remove items\nfruits.remove('banana')\n```\n\nLists are mutable, meaning you can change their contents."
    },
    {
        "lesson_id": 4,
        "topic": "Python Loops",
        "content": "Loops allow you to repeat code multiple times. Python has two main types of loops:\n\n**For Loop:**\n```python\nfor i in range(5):\n    print(i)  # Prints 0, 1, 2, 3, 4\n\nfruits = ['apple', 'banana', 'orange']\nfor fruit in fruits:\n    print(fruit)\n```\n\n**While Loop:**\n```python\ncount = 0\nwhile count < 5:\n    print(count)\n    count += 1\n```\n\nLoops help you avoid repetitive code."
    }
]

print("Creating sample lesson data...")
for lesson_data in sample_lessons:
    lesson, created = LessonChunk.objects.get_or_create(
        lesson_id=lesson_data["lesson_id"],
        topic=lesson_data["topic"],
        defaults={"content": lesson_data["content"]}
    )
    if created:
        print(f"Created lesson: {lesson.topic}")
    else:
        print(f"Lesson already exists: {lesson.topic}")

print(f"Total lessons in database: {LessonChunk.objects.count()}")
