import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import User

print("Listing all users:")
for user in User.objects.all():
    print(f"ID: {user.id} | Username: {user.username} | Email: {user.email}")
