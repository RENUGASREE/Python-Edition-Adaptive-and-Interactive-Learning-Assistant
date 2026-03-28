import os, sys, django, traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "python_edition_django.settings")
django.setup()

from django.contrib.auth import get_user_model
from analytics.analytics_services import mastery_progression

User = get_user_model()
user = User.objects.first()

try:
    print("Testing mastery_progression...")
    res = mastery_progression(user)
    print("Result:", res)
except Exception:
    traceback.print_exc()
