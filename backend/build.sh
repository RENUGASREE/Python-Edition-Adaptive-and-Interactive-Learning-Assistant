#!/usr/bin/env bash
# exit on error
set -o errexit

python -m pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py ensure_superuser --noinput
python manage.py seed_platform_data
python manage.py seed_curriculum_data
python manage.py seed_placement_quiz
