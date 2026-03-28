import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import Module, Lesson, Challenge

BATCH10_DATA = [
    { "module_id": 21, "topics": [
        { "title": "List Comprehension", "beginner": {"content": "🟢 BEGINNER LEVEL\n- New list from old: [x for x in L].", "challenge": {"title": "L-Comp Basic", "description": "[x for x in [1,2,3]].", "initial_code": "# code", "solution_code": "print([x for x in [1,2,3]])", "test_cases": [{"input": "", "expected": "[1, 2, 3]"}]}}, "intermediate": {"content": "🟡 INTERMEDIATE LEVEL\n- With if condition: [x for x in L if x > 1].", "challenge": {"title": "L-Comp If", "description": "[x for x in [1,2,3] if x>1].", "initial_code": "# code", "solution_code": "print([x for x in [1,2,3] if x>1])", "test_cases": [{"input": "", "expected": "[2, 3]"}]}}, "pro": {"content": "🔴 PRO LEVEL\n- Nested list comprehension.", "challenge": {"title": "L-Comp Nested", "description": "[[x] for x in [1,2]].", "initial_code": "# code", "solution_code": "print([[x] for x in [1,2]])", "test_cases": [{"input": "", "expected": "[[1], [2]]"}]}} },
        { "title": "Dict Comprehension", "beginner": {"content": "🟢 BEGINNER LEVEL\n- {k:v for k,v in items}.", "challenge": {"title": "D-Comp Basic", "description": "{x:x*x for x in [1,2]}.", "initial_code": "# code", "solution_code": "print({x:x*x for x in [1,2]})", "test_cases": [{"input": "", "expected": "{1: 1, 2: 4}"}]}}, "intermediate": {"content": "🟡 INTERMEDIATE LEVEL\n- Swap k and v using dict comp.", "challenge": {"title": "D-Comp Swap", "description": "{v:k for k,v in {1:'a'}.items()}.", "initial_code": "# code", "solution_code": "print({v:k for k,v in {1:'a'}.items()})", "test_cases": [{"input": "", "expected": "{'a': 1}"}]}}, "pro": {"content": "🔴 PRO LEVEL\n- Filtered dict comp.", "challenge": {"title": "D-Comp Filter", "description": "{x:x for x in [1,2,3] if x>1}.", "initial_code": "# code", "solution_code": "print({x:x for x in [1,2,3] if x>1})", "test_cases": [{"input": "", "expected": "{2: 2, 3: 3}"}]}} }
    ]},
    { "module_id": 22, "topics": [
        { "title": "Recursion", "beginner": {"content": "🟢 BEGINNER LEVEL\n- Function calling itself.", "challenge": {"title": "Recur Hello", "description": "Just print 'Recursion Intro'.", "initial_code": "print('Recursion Intro')", "solution_code": "print('Recursion Intro')", "test_cases": [{"input": "", "expected": "Recursion Intro"}]}}, "intermediate": {"content": "🟡 INTERMEDIATE LEVEL\n- Base case vs Recursive case.", "challenge": {"title": "Factorial 3", "description": "Calculate 3! using recursion or logic.", "initial_code": "def f(n): return 1 if n<=1 else n*f(n-1)\nprint(f(3))", "solution_code": "def f(n): return 1 if n<=1 else n*f(n-1)\nprint(f(3))", "test_cases": [{"input": "", "expected": "6"}]}}, "pro": {"content": "🔴 PRO LEVEL\n- Recursion limit and Tail recursion.", "challenge": {"title": "Fibonacci 5", "description": "Print 5th Fib num (0,1,1,2,3,5).", "initial_code": "# code", "solution_code": "def fib(n): return n if n<=1 else fib(n-1)+fib(n-2)\nprint(fib(5))", "test_cases": [{"input": "", "expected": "5"}]}} }
    ]}
]

def populate_batch10():
    print("🚀 Starting Batch 10 Population...")
    tl=0; tc=0
    for med in BATCH10_DATA:
        mid = med["module_id"]
        for topic in med["topics"]:
            title = topic["title"]
            for level in ["beginner", "intermediate", "pro"]:
                dl = level.capitalize()
                Lesson.objects.filter(module_id=mid, title=title, difficulty=dl).delete()
                l = Lesson.objects.create(module_id=mid, title=title, difficulty=dl, content=topic[level]["content"], slug=title.lower().replace(" ", "-"), order=70, duration=15)
                tl += 1
                c_data = topic[level]["challenge"]
                Challenge.objects.filter(lesson_id=l.id).delete()
                Challenge.objects.create(lesson_id=l.id, title=c_data["title"], description=c_data["description"], initial_code=c_data["initial_code"], solution_code=c_data["solution_code"], test_cases=c_data["test_cases"], points=100, difficulty=dl)
                tc += 1
    print(f"✅ Created {tl} Lessons and {tc} Challenges.")

if __name__ == "__main__":
    populate_batch10()
