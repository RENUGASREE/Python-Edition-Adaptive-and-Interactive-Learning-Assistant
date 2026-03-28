import os
import sys
import django

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import Module, Lesson, Challenge

MASSIVE_DATA = [
    { "module_id": 19, "topics": [
        { "title": "Arithmetic Operators", "beginner": {"content": "🟢 BEGINNER LEVEL\n\n- Definition: Basic math symbols (+, -, *, /).\n- Explanation: Used to calculate results.\n- Example: 5 + 3 = 8.", "challenge": {"title": "Add Ops", "description": "Print 10 + 20.", "initial_code": "print(10 + 20)", "solution_code": "print(10 + 20)", "test_cases": [{"input": "", "expected": "30"}]}}, "intermediate": {"content": "🟡 INTERMEDIATE LEVEL\n\n- Modulo (%) and Floor Division (//).\n- Example: 10 // 3 = 3.", "challenge": {"title": "Floor Div", "description": "Print floor division of 11 by 3.", "initial_code": "print(11 // 3)", "solution_code": "print(11 // 3)", "test_cases": [{"input": "", "expected": "3"}]}}, "pro": {"content": "🔴 PRO LEVEL\n\n- Operator Precedence and Power (**).\n- Example: 2**3 = 8.", "challenge": {"title": "Power Op", "description": "Print 2 to the power 5.", "initial_code": "print(2**5)", "solution_code": "print(2**5)", "test_cases": [{"input": "", "expected": "32"}]}} },
        { "title": "Logical Operators", "beginner": {"content": "🟢 BEGINNER LEVEL\n- AND, OR, NOT basics.", "challenge": {"title": "And Op", "description": "Print True and False.", "initial_code": "print(True and False)", "solution_code": "print(True and False)", "test_cases": [{"input": "", "expected": "False"}]}}, "intermediate": {"content": "🟡 INTERMEDIATE LEVEL\n- Chained logic (age > 10 and age < 20).", "challenge": {"title": "Chain Logic", "description": "Print 5 < 10 and 10 < 15.", "initial_code": "print(5 < 10 and 10 < 15)", "solution_code": "print(5 < 10 and 10 < 15)", "test_cases": [{"input": "", "expected": "True"}]}}, "pro": {"content": "🔴 PRO LEVEL\n- Short-circuiting evaluation.", "challenge": {"title": "Short Circuit", "description": "Print True or False and True.", "initial_code": "print(True or False and True)", "solution_code": "print(True or (False and True))", "test_cases": [{"input": "", "expected": "True"}]}} }
    ]},
    { "module_id": 22, "topics": [
        { "title": "Lambda Functions", "beginner": {"content": "🟢 BEGINNER LEVEL\n- Small anonymous functions.", "challenge": {"title": "Lambda add", "description": "f = lambda x: x + 10. Print f(5).", "initial_code": "f = lambda x: x + 10\nprint(f(5))", "solution_code": "f = lambda x: x + 10\nprint(f(5))", "test_cases": [{"input": "", "expected": "15"}]}}, "intermediate": {"content": "🟡 INTERMEDIATE LEVEL\n- Using lambda with map().", "challenge": {"title": "Map Lambda", "description": "L=[1,2]. Map lambda x: x*2 to L and print list.", "initial_code": "L = [1, 2]\nprint(list(map(lambda x: x*2, L)))", "solution_code": "L = [1, 2]\nprint(list(map(lambda x: x*2, L)))", "test_cases": [{"input": "", "expected": "[2, 4]"}]}}, "pro": {"content": "🔴 PRO LEVEL\n- Using lambda with filter/reduce.", "challenge": {"title": "Filter Lambda", "description": "Filter odd nums from [1,2,3,4].", "initial_code": "L = [1, 2, 3, 4]\nprint(list(filter(lambda x: x%2 != 0, L)))", "solution_code": "L = [1, 2, 3, 4]\nprint(list(filter(lambda x: x%2 != 0, L)))", "test_cases": [{"input": "", "expected": "[1, 3]"}]}} }
    ]}
]

def populate_massive():
    print("🚀 Starting Massive Population Batch 1...")
    tl=0; tc=0
    for med in MASSIVE_DATA:
        mid = med["module_id"]
        for topic in med["topics"]:
            title = topic["title"]
            for level in ["beginner", "intermediate", "pro"]:
                dl = level.capitalize()
                Lesson.objects.filter(module_id=mid, title=title, difficulty=dl).delete()
                l = Lesson.objects.create(module_id=mid, title=title, difficulty=dl, content=topic[level]["content"], slug=title.lower().replace(" ", "-"), order=80, duration=15)
                tl += 1
                c_data = topic[level]["challenge"]
                Challenge.objects.filter(lesson_id=l.id).delete()
                Challenge.objects.create(lesson_id=l.id, title=c_data["title"], description=c_data["description"], initial_code=c_data["initial_code"], solution_code=c_data["solution_code"], test_cases=c_data["test_cases"], points=150, difficulty=dl)
                tc += 1
    print(f"✅ Created {tl} Lessons and {tc} Challenges.")

if __name__ == "__main__":
    populate_massive()
