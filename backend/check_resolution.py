import os, django, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import User
from recommendation.services import _get_module_difficulty

topics = [
    'variables', 'conditions', 'loops', 'functions', 'oop',
    'introduction', 'file_handling', 'error_handling', 'advanced_python', 'data_structures'
]

for user in User.objects.all():
    md = (user.mastery_vector or {}).get('_module_difficulty', {})
    if not md:
        print(f"{user.username}: no _module_difficulty stored")
        continue
    print(f"User: {user.username} | global level: {user.level}")
    print(f"Stored keys: {list(md.keys())}")
    print()
    for t in topics:
        result = _get_module_difficulty(user, t)
        print(f"  {t:<25} => {result}")
    print()

sys.stdout.flush()
