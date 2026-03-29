import os, django, traceback
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import User
from recommendation.services import recommend_next

with open("test_recommend_utf8.log", "w", encoding="utf-8") as f:
    f.write("Testing recommend_next for each user...\n")
    for user in User.objects.all():
        f.write(f"\n--- User: {user.username} ---\n")
        try:
            result = recommend_next(user)
            f.write(f"  next_topic:              {result.get('next_topic')}\n")
            f.write(f"  difficulty_level:        {result.get('difficulty_level')}\n")
            f.write(f"  module_difficulty_assigned: {result.get('reason_for_recommendation', {}).get('module_difficulty_assigned')}\n")
            f.write(f"  recommended_lesson_title: {result.get('recommended_lesson_title')}\n")
            f.write(f"  reason_codes:            {result.get('reason_codes')}\n")
        except Exception:
            f.write("  ERROR:\n")
            f.write(traceback.format_exc() + "\n")
