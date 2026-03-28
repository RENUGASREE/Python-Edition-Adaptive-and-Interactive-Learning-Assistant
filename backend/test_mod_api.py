import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "python_edition_django.settings")
django.setup()

from django.contrib.auth import get_user_model
from core.serializers import ModuleSerializer
from core.models import Module

User = get_user_model()
user = User.objects.first()

class DummyRequest:
    def __init__(self, user):
        self.user = user

req = DummyRequest(user)
modules = Module.objects.all().order_by('order')[:2]

serializer = ModuleSerializer(modules, many=True, context={'request': req})
data = serializer.data

for m in data:
    print(f"Module {m['id']} - {m['title']}: {len(m['lessons'])} lessons")
    for l in m['lessons'][:2]:
        print(f"  Lesson {l['id']} - {l['title']}, unlocked: {l.get('unlocked')}, diff: {l.get('difficulty')}")
