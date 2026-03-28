#!/usr/bin/env python
"""
Exhaustive Curriculum Enhancer (180 Lessons)
----------------------------
Generates 3 tiers (Beginner, Intermediate, Pro) for every one of the 60 topics.
"""

import os, sys, django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "python_edition_django.settings")
django.setup()

from core.models import Lesson, Module

# ────────────────────────────────────────────────────────────────────────────────
# 3-TIER CONTENT GENERATOR
# ────────────────────────────────────────────────────────────────────────────────

def get_tiered_content(title, level):
    if level == "Beginner":
        return f"""## 🎯 Learning Objectives (Beginner)
- Understand basic syntax and concepts of **{title}**.
- Run your first code snippet using **{title}**.

---

## 📖 Concept Explanation: What is {title}?
**{title}** is a fundamental building block in Python. At this level, we focus on the basic syntax and clear usage.

### Key Points
- Simple and readable code.
- Focus on understanding "Why" we use it.

---

## 💡 Practical Example: Beginner's Simple Logic
```python
# Initializing {title}
print(f"Starting {title} at Beginner level...")
data = "Hello World"
print(data)
```

---

## 📝 Key Takeaways
- Mastery starts with the basics of **{title}**.
- Don't skip the fundamentals!
"""
    elif level == "Intermediate":
        return f"""## 🎯 Learning Objectives (Intermediate)
- Apply **{title}** to solve practical problems.
- Use advanced methods and built-in functions related to **{title}**.

---

## 📖 Concept Explanation: Practical Application
Now that you know the basics, let's explore how **{title}** handles real-world scenarios efficiently.

### Key points
- Optimization and best practices.
- Handling edge cases and user inputs.

---

## 💡 Practical Example: Functional Tooling
```python
# Processing data with {title}
def process_data(input_val):
    print(f"Processing {title} for: {{input_val}}")
    return input_val.upper()

result = process_data("inter_val")
print(result)
```

---

## 📝 Key Takeaways
- **{title}** is more powerful when combined with functions.
- Efficiency matters at this level.
"""
    else: # Pro
        return f"""## 🎯 Learning Objectives (Pro)
- Build robust, production-ready systems using **{title}**.
- Optimize for performance, memory, and security.

---

## 📖 Concept Explanation: Advanced Engineering
At the Pro level, **{title}** is about high-performance engineering. We look at memory management, complex logic, and deep integration.

### Key points
- Scalability and robustness.
- Advanced Pythonic patterns.

---

## 💡 Practical Example: High-Performance Solution
```python
# Engineering-grade {title}
import time

def high_performance_task():
    # Complex {title} logic
    start = time.perf_counter()
    print(f"Executing Pro-level {title} task...")
    # ... logic ...
    end = time.perf_counter()
    print(f"Completed in {{end - start:.4f}}s")

if __name__ == "__main__":
    high_performance_task()
```

---

## 📝 Key Takeaways
- Pro-level **{title}** requires deep thinking and optimization.
- Always focus on scalability.
"""

# TOPIC LIBRARY
TOPICS = [
    "Strings Basics", "Variables", "Operators", "Input/Output", "Data Types",
    "if / else", "Loops", "Functions", "Modules", "OOP Basics",
    "List Operations", "Tuples", "Sets", "Dictionaries", "Inheritance",
    "Polymorphism", "Encapsulation", "Abstraction", "Lambda Functions", "List Comprehensions",
    "Error Handling", "File I/O", "JSON Processing", "Pandas Intro", "NumPy Basics",
    "Matplotlib Basics", "API Integration", "Asyncio", "Decorators", "Generators",
    "Context Managers", "Virtual Environments", "PyTest Basics", "Logging", "Regular Expressions",
    "Multi-threading", "Multi-processing", "Database Interaction (SQLite)", "SQLite Advanced", "SQLAlchemy",
    "Flask Intro", "Django Basics", "Web Scraping", "Automation (Selenium)", "Data Cleaning",
    "Feature Engineering", "Linear Regression", "Decision Trees", "K-Means Clustering", "Neural Networks Intro",
    "NLP Basics", "OpenCV Basics", "Stock Market Analysis", "Face Recognition", "Chatbot Development",
    "PyGame Intro", "Security & Encryption", "Deployment basics", "CI/CD Pipelines", "Docker Basics"
]

def update_lessons_180():
    # We clear the existing lessons to prevent ID collisions or confusion, 
    # OR we can just update them. Since I want 180, and I have 60, I'll create the new ones.
    
    # First, let's map modules to topics (simple distribution)
    modules = Module.objects.all().order_by('order')
    if not modules:
        print("No modules found. Please run migrations.")
        return
        
    # CLEAR OLD LESSONS to start fresh (Clean state for the 180 expansion)
    # Lesson.objects.all().delete()
    
    count = 0
    levels = ["Beginner", "Intermediate", "Pro"]
    
    for i, topic_name in enumerate(TOPICS):
        # Distribute topics across modules
        mod_idx = i // (len(TOPICS) // len(modules)) if len(modules) > 0 else 0
        mod_idx = min(mod_idx, len(modules) - 1)
        module = modules[mod_idx]
        
        for level in levels:
            full_title = topic_name # Clean title
            l_slug = f"{topic_name.lower().replace(' ', '-')}-{level.lower()}"
            
            # Use get_or_create to allow partial updates
            lesson, created = Lesson.objects.update_or_create(
                slug=l_slug,
                defaults={
                    "title": full_title,
                    "module_id": module.id,
                    "content": get_tiered_content(topic_name, level),
                    "order": i * 3 + levels.index(level),
                    "difficulty": level,
                    "duration": 15
                }
            )
            print(f"[{'NEW' if created else 'UPD'}] {full_title} ({level})")
            count += 1
            
    print(f"\nExpansion Complete! {count} lessons processed.")

if __name__ == "__main__":
    update_lessons_180()
