import os
import sys
import django
from django.core.management import call_command
from django.contrib.auth import get_user_model

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

def setup_production():
    # 1. Run migrations
    print("🚀 Running migrations...")
    try:
        call_command('migrate', interactive=False)
        print("✅ Migrations completed.")
    except Exception as e:
        print(f"❌ Error running migrations: {e}")

    # 2. Create Superuser if not exists
    User = get_user_model()
    admin_user = os.getenv("ADMIN_USERNAME", "admin")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
    admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")

    if not User.objects.filter(username=admin_user).exists():
        print(f"👤 Creating superuser: {admin_user}...")
        User.objects.create_superuser(admin_user, admin_email, admin_password)
        print("✅ Superuser created.")
    else:
        print("ℹ️ Superuser already exists.")

    # 3. Seed Placement Quiz
    print("🎯 Seeding Placement Quiz...")
    try:
        call_command('seed_placement_quiz')
        print("✅ Placement Quiz seeded.")
    except Exception as e:
        print(f"❌ Error seeding placement quiz: {e}")

    # 4. Seed Curriculum Data (Lessons, Modules, Challenges)
    print("📚 Seeding Curriculum Data...")
    try:
        # We run it with --reset to clean up any old/incorrect module IDs from previous deploys.
        call_command('seed_curriculum_data', reset=True)
        print("✅ Curriculum data seeded.")
    except Exception as e:
        print(f"❌ Error seeding curriculum data: {e}")

    # 5. Seed Platform Data (Additional items)
    print("🛠️ Seeding Platform Data...")
    try:
        call_command('seed_platform_data')
        print("✅ Platform data seeded.")
    except Exception as e:
        print(f"❌ Error seeding platform data: {e}")

    # 6. Final Sync
    try:
        from core.models import Certificate
        import uuid
        print("📜 Syncing Certificate Verification Codes...")
        certs_to_update = Certificate.objects.filter(verification_code__isnull=True)
        if certs_to_update.exists():
            for cert in certs_to_update:
                cert.verification_code = uuid.uuid4()
                cert.save()
            print(f"✅ Synced {certs_to_update.count()} certificates.")
    except Exception as e:
        print(f"❌ Error syncing certificates: {e}")

    print("🏁 Setup production finished.")

if __name__ == "__main__":
    setup_production()
