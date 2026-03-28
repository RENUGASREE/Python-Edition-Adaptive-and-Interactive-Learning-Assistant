import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import User

print("Searching for users with 'python' in their username or email:")
users = User.objects.filter(models.Q(username__icontains='python') | models.Q(email__icontains='python'))
for user in users:
    print(f"ID: {user.id} | Username: {user.username} | Email: {user.email}")

if not users.exists():
    print("No users found with 'python' in their username or email.")
