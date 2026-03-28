import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import User, UserProgress, QuizAttempt, UserMastery, DiagnosticAttempt, Progress, Recommendation, Certificate, ChatMessage

def reset_user(username):
    try:
        user = User.objects.get(username=username)
        user_id_str = str(user.id)
        original_uuid = user.original_uuid
        
        print(f"--- Resetting User: {username} (ID: {user.id}) ---")
        
        # 1. UserProgress (using numeric ID as string and original_uuid)
        up_deleted = UserProgress.objects.filter(user_id=user_id_str).delete()[0]
        if original_uuid:
            up_deleted += UserProgress.objects.filter(user_id=original_uuid).delete()[0]
        print(f"Deleted {up_deleted} UserProgress records.")
        
        # 2. QuizAttempt
        qa_deleted = QuizAttempt.objects.filter(user=user).delete()[0]
        print(f"Deleted {qa_deleted} QuizAttempt records.")
        
        # 3. UserMastery
        um_deleted = UserMastery.objects.filter(user=user).delete()[0]
        print(f"Deleted {um_deleted} UserMastery records.")
        
        # 4. DiagnosticAttempt
        da_deleted = DiagnosticAttempt.objects.filter(user=user).delete()[0]
        print(f"Deleted {da_deleted} DiagnosticAttempt records.")
        
        # 5. Progress (Topic Mastery)
        p_deleted = Progress.objects.filter(user=user).delete()[0]
        print(f"Deleted {p_deleted} topic Progress records.")
        
        # 6. Recommendations
        r_deleted = Recommendation.objects.filter(user=user).delete()[0]
        print(f"Deleted {r_deleted} Recommendation records.")
        
        # 7. Certificates
        c_deleted = Certificate.objects.filter(user=user).delete()[0]
        print(f"Deleted {c_deleted} Certificate records.")
        
        # 8. Chat Messages
        cm_deleted = ChatMessage.objects.filter(user=user).delete()[0]
        print(f"Deleted {cm_deleted} ChatMessage records.")
        
        # 9. Reset User Fields
        user.diagnostic_completed = False
        user.has_taken_quiz = False
        user.mastery_vector = {}
        user.engagement_score = 0.5
        user.learning_velocity = 0.0
        user.level = "Beginner"
        user.save()
        
        print(f"--- Reset Complete for '{username}' ---")
        
    except User.DoesNotExist:
        print(f"Error: User '{username}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # The database records user 'Python' with a capital 'P'
    reset_user("Python")
