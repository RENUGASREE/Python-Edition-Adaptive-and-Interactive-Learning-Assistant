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
    from core.models import Lesson

    if not Lesson.objects.exists():
        logging.getLogger(__name__).info('No lessons found; seeding curriculum data...')
        call_command('seed_curriculum_data', verbosity=0)
except (OperationalError, ProgrammingError):
    # Database is not ready yet (migrations may be running) or not accessible.
    pass
except Exception as e:
    # Catch-all to avoid breaking the WSGI process if seeding fails.
    logging.getLogger(__name__).exception('Failed to seed curriculum data: %s', e)
