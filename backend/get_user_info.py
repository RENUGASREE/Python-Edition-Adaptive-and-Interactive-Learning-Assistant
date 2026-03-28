import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import User

user_17 = User.objects.get(id=17)
print(f"User 17 Username: '{user_17.username}'")
print(f"User 17 Email: '{user_17.email}'")

user_12 = User.objects.get(id=12)
print(f"User 12 Username: '{user_12.username}'")
print(f"User 12 Email: '{user_12.email}'")
