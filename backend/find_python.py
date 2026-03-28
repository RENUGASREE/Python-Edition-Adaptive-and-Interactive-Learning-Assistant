import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import User

print("Finding user 'Python'...")
try:
    u = User.objects.get(username__iexact='Python')
    print(f"Found: ID {u.id}, Username: {u.username}, Email: {u.email}")
except User.DoesNotExist:
    print("User 'Python' not found.")
    
print("\nAll users:")
for u in User.objects.all():
    print(f"ID {u.id}: '{u.username}' ('{u.email}')")
