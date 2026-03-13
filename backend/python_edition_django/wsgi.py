"""
WSGI config for python_edition_django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import logging

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')

application = get_wsgi_application()

# Ensure the platform curriculum is seeded on startup (useful for fresh deployments)
# This runs only when the WSGI app is started (e.g., gunicorn on Render), not during manage.py migrate.
try:
    from django.core.management import call_command
    from django.db import OperationalError, ProgrammingError
    from django.contrib.auth import get_user_model
    from core.models import Lesson

    if not Lesson.objects.exists():
        logging.getLogger(__name__).info('No lessons found; seeding curriculum data...')
        call_command('seed_curriculum_data', verbosity=0)

    # Create an admin user automatically if env vars are provided and no superuser exists.
    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        admin_username = os.environ.get('ADMIN_USERNAME')
        admin_email = os.environ.get('ADMIN_EMAIL')
        admin_password = os.environ.get('ADMIN_PASSWORD')
        if admin_username and admin_email and admin_password:
            logging.getLogger(__name__).info('Creating superuser from environment variables...')
            User.objects.create_superuser(username=admin_username, email=admin_email, password=admin_password)
            logging.getLogger(__name__).info('Superuser created: %s', admin_username)
        else:
            logging.getLogger(__name__).info('No superuser exists and ADMIN_* env vars not set; skipping superuser creation.')

except (OperationalError, ProgrammingError):
    # Database is not ready yet (migrations may be running) or not accessible.
    pass
except Exception as e:
    # Catch-all to avoid breaking the WSGI process if seeding fails.
    logging.getLogger(__name__).exception('Failed to seed curriculum data or create superuser: %s', e)
