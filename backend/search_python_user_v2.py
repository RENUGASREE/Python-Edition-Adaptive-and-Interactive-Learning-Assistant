import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import User
from django.db.models import Q

print("All Users in the system:")
for user in User.objects.all():
    print(f"ID: {user.id} | Username: '{user.username}' | Email: '{user.email}'")

print("\nSearching for users with 'python' in their username or email:")
users = User.objects.filter(Q(username__icontains='python') | Q(email__icontains='python'))
for user in users:
    print(f"ID: {user.id} | Username: '{user.username}' | Email: '{user.email}'")

if not users.exists():
    print("No users found with 'python' in their username or email.")
