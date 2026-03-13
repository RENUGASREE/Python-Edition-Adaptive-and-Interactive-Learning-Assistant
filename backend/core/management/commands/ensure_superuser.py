from __future__ import annotations

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
  help = "Ensure at least one Django superuser exists. Can run non-interactively on Render."

  def add_arguments(self, parser):
    parser.add_argument(
      "--noinput",
      action="store_true",
      help="Create a superuser non-interactively using DJANGO_SUPERUSER_* env vars if needed.",
    )

  def handle(self, *args, **options):
    User = get_user_model()
    if User.objects.filter(is_superuser=True).exists():
      self.stdout.write(self.style.SUCCESS("Superuser already exists; no action taken."))
      return

    noinput = options.get("noinput", False)

    if noinput:
      username = os.getenv("DJANGO_SUPERUSER_USERNAME")
      email = os.getenv("DJANGO_SUPERUSER_EMAIL")
      password = os.getenv("DJANGO_SUPERUSER_PASSWORD")
      if not username or not password:
        self.stdout.write(
          self.style.WARNING(
            "No superuser exists and DJANGO_SUPERUSER_USERNAME / DJANGO_SUPERUSER_PASSWORD are not set. "
            "Skipping creation in --noinput mode."
          )
        )
        return
      if not email:
        email = f"{username}@example.com"
      User.objects.create_superuser(username=username, email=email, password=password)
      self.stdout.write(
        self.style.SUCCESS(f"Superuser '{username}' created from environment variables.")
      )
      return

    # Interactive mode (local development).
    self.stdout.write("No superuser exists. Enter credentials to create one.")
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    if not username or not password:
      self.stdout.write(self.style.ERROR("Username and password are required; aborting."))
      return
    User.objects.create_superuser(username=username, email=email or None, password=password)
    self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created."))

