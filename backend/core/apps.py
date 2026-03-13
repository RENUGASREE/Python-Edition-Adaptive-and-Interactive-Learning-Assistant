import os
import sys
import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Automatically seed curriculum content and/or create a superuser in production.
        # Only run in a server runtime (gunicorn/runserver), not during migrations or management commands.
        if any(arg in sys.argv for arg in ("makemigrations", "migrate", "collectstatic", "test", "shell")):
            return

        # Auto-create a superuser if requested via environment variables.
        if os.getenv("CREATE_SUPERUSER_ON_STARTUP", "").strip().lower() in ("1", "true", "yes"):
            try:
                from django.contrib.auth import get_user_model

                User = get_user_model()
                username = os.getenv("SUPERUSER_USERNAME")
                email = os.getenv("SUPERUSER_EMAIL")
                password = os.getenv("SUPERUSER_PASSWORD")

                if username and email and password and not User.objects.filter(username=username).exists():
                    User.objects.create_superuser(username=username, email=email, password=password)
                    logger.info("Created superuser %s", username)
            except Exception as e:
                logger.exception("Failed to create superuser on startup: %s", e)

        # Auto-seed curriculum data if requested and if it's missing.
        if os.getenv("SEED_CURRICULUM_ON_STARTUP", "").strip().lower() in ("1", "true", "yes"):
            try:
                from django.core.management import call_command
                from core.models import Lesson

                if not Lesson.objects.exists():
                    call_command("seed_curriculum_data")
                    logger.info("Seeded curriculum data on startup")
            except Exception as e:
                logger.exception("Failed to seed curriculum data on startup: %s", e)
