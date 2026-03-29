import os, django, traceback
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import User
from recommendation.services import recommend_next

print("Testing recommend_next for each user...")
for user in User.objects.all():
    print(f"\n--- User: {user.username} ---")
    try:
        result = recommend_next(user)
        print(f"  next_topic:              {result.get('next_topic')}")
        print(f"  difficulty_level:        {result.get('difficulty_level')}")
        print(f"  module_difficulty_assigned: {result.get('reason_for_recommendation', {}).get('module_difficulty_assigned')}")
        print(f"  recommended_lesson_title: {result.get('recommended_lesson_title')}")
        print(f"  reason_codes:            {result.get('reason_codes')}")
    except Exception:
        print("  ERROR:")
        traceback.print_exc()
