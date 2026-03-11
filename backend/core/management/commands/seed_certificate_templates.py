from django.core.management.base import BaseCommand
from core.models import CertificateTemplate

TEMPLATES = [
    ("beginner-python", "Beginner Python Certificate", "Awarded for completing beginner track"),
    ("intermediate-python", "Intermediate Python Certificate", "Awarded for completing intermediate track"),
    ("advanced-python", "Advanced Python Certificate", "Awarded for completing advanced track"),
    ("module-completion", "Module Completion Certificate", "Awarded for completing any module"),
    ("full-course", "Full Course Completion Certificate", "Awarded for completing the full curriculum"),
]

class Command(BaseCommand):
    help = "Seed certificate templates"

    def handle(self, *args, **options):
        for code, title, desc in TEMPLATES:
            CertificateTemplate.objects.get_or_create(code=code, defaults={"title": title, "description": desc})
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(TEMPLATES)} certificate templates"))
