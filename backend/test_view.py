import os, sys, django, traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "python_edition_django.settings")
django.setup()

from django.contrib.auth import get_user_model
from analytics.views import AnalyticsView

User = get_user_model()
user = User.objects.first()

class DummyRequest:
    def __init__(self, user):
        self.user = user

try:
    req = DummyRequest(user)
    view = AnalyticsView()
    resp = view.get(req)
    print("Response keys:", resp.data.keys())
    print("Learning gain:", resp.data["learningGain"])
except Exception as e:
    traceback.print_exc()
