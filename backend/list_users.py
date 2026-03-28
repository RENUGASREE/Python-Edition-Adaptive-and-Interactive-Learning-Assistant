import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import User

users = User.objects.all()
for user in users:
    print(f"Username: '{user.username}', Email: '{user.email}'")
