import os, sys, django, traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "python_edition_django.settings")
django.setup()

from django.contrib.auth import get_user_model
from core.models import UserProgress, QuizAttempt
from datetime import datetime

User = get_user_model()
user = User.objects.first()

try:
    user_id = user.original_uuid or str(user.id)
    print("Testing has_lessons check...")
    has_lessons = UserProgress.objects.filter(
        user_id=user_id, completed=True
    ).exists()
    print("has_lessons:", has_lessons)
    
    print("Testing has_module_attempts check...")
    has_module_attempts = QuizAttempt.objects.filter(user=user).exists()
    print("has_module_attempts:", has_module_attempts)
    
except Exception as e:
    traceback.print_exc()
