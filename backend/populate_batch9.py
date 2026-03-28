import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import Module, Lesson, Challenge

BATCH9_DATA = [
    { "module_id": 21, "topics": [
        { "title": "Dict Methods", "beginner": {"content": "🟢 BEGINNER LEVEL\n- .get(key) for safety.", "challenge": {"title": "Get Key", "description": "d={'a':1}. Print d.get('b', 0).", "initial_code": "d = {'a': 1}\n# print", "solution_code": "d = {'a': 1}\nprint(d.get('b', 0))", "test_cases": [{"input": "", "expected": "0"}]}}, "intermediate": {"content": "🟡 INTERMEDIATE LEVEL\n- .keys(), .values(), .items().", "challenge": {"title": "Loop Dict", "description": "Print keys of {'a':1}.", "initial_code": "d = {'a': 1}\n# loop", "solution_code": "d = {'a': 1}\nfor k in d.keys(): print(k)", "test_cases": [{"input": "", "expected": "a"}]}}, "pro": {"content": "🔴 PRO LEVEL\n- update() and pop().", "challenge": {"title": "Pop Item", "description": "d={'a':1}. d.pop('a'). Print d.", "initial_code": "d = {'a': 1}\n# pop", "solution_code": "d = {'a': 1}\nd.pop('a')\nprint(d)", "test_cases": [{"input": "", "expected": "{}"}]}} },
        { "title": "Lambda Functions", "beginner": {"content": "🟢 BEGINNER LEVEL\n- f = lambda x: x + 1.", "challenge": {"title": "Simple Lambda", "description": "Lambda to add 5 to x=10 and print.", "initial_code": "f = lambda x: x + 5\n# print", "solution_code": "f = lambda x: x + 5\nprint(f(10))", "test_cases": [{"input": "", "expected": "15"}]}}, "intermediate": {"content": "🟡 INTERMEDIATE LEVEL\n- Using lambda in sort(key=...).", "challenge": {"title": "Sort Lambda", "description": "Just print 'Lambda sorted'.", "initial_code": "print('Lambda sorted')", "solution_code": "print('Lambda sorted')", "test_cases": [{"input": "", "expected": "Lambda sorted"}]}}, "pro": {"content": "🔴 PRO LEVEL\n- Higher order lambdas.", "challenge": {"title": "H.O. Lambda", "description": "Print '(lambda x: x*2)(5)'.", "initial_code": "# code", "solution_code": "print((lambda x: x*2)(5))", "test_cases": [{"input": "", "expected": "10"}]}} }
    ]}
]

def populate_batch9():
    print("🚀 Starting Batch 9 Population...")
    tl=0; tc=0
    for med in BATCH9_DATA:
        mid = med["module_id"]
        for topic in med["topics"]:
            title = topic["title"]
            for level in ["beginner", "intermediate", "pro"]:
                dl = level.capitalize()
                Lesson.objects.filter(module_id=mid, title=title, difficulty=dl).delete()
                l = Lesson.objects.create(module_id=mid, title=title, difficulty=dl, content=topic[level]["content"], slug=title.lower().replace(" ", "-"), order=60, duration=15)
                tl += 1
                c_data = topic[level]["challenge"]
                Challenge.objects.filter(lesson_id=l.id).delete()
                Challenge.objects.create(lesson_id=l.id, title=c_data["title"], description=c_data["description"], initial_code=c_data["initial_code"], solution_code=c_data["solution_code"], test_cases=c_data["test_cases"], points=100, difficulty=dl)
                tc += 1
    print(f"✅ Created {tl} Lessons and {tc} Challenges.")

if __name__ == "__main__":
    populate_batch9()
