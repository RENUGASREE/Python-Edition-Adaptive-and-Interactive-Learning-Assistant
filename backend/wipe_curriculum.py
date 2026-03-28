import os
import django
import sys

# Set up Django environment
# Add the current directory (backend) to the path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import Module, Lesson, Challenge, Quiz, Question, UserProgress, Progress, UserMastery, DiagnosticAttempt

def wipe_data():
    print("Wiping all existing curriculum and progress data...")
    
    # Delete model instances in order of dependencies
    UserProgress.objects.all().delete()
    Progress.objects.all().delete()
    UserMastery.objects.all().delete()
    DiagnosticAttempt.objects.all().delete()
    
    Question.objects.all().delete()
    Quiz.objects.all().delete()
    Challenge.objects.all().delete()
    Lesson.objects.all().delete()
    Module.objects.all().delete()
    
    print("Cleanup complete. The database is now ready for a professional rebuild.")

if __name__ == "__main__":
    wipe_data()
