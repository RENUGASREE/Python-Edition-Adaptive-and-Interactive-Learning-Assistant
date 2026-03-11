from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    level = models.CharField(max_length=50, default="Beginner")
    original_uuid = models.CharField(max_length=36, blank=True, null=True, unique=True)
    engagement_score = models.FloatField(default=0.5)
    diagnostic_completed = models.BooleanField(default=False)
    has_taken_quiz = models.BooleanField(default=False)
    learning_velocity = models.FloatField(default=0.0)
    mastery_vector = models.JSONField(default=dict, blank=True)
    profileImageUrl = models.FileField(upload_to="avatars/", blank=True, null=True)

# --- Content Models (Mapped to existing tables) ---

class Module(models.Model):
    title = models.TextField()
    description = models.TextField()
    order = models.IntegerField(db_index=True)
    image_url = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'modules'
        ordering = ["order", "id"]

class Lesson(models.Model):
    module_id = models.IntegerField(db_index=True)
    title = models.TextField()
    slug = models.TextField()
    content = models.TextField()
    order = models.IntegerField(db_index=True)
    difficulty = models.TextField(blank=True, null=True)
    duration = models.IntegerField()

    class Meta:
        db_table = 'lessons'

class Quiz(models.Model):
    lesson_id = models.IntegerField(db_index=True)
    title = models.TextField()

    class Meta:
        db_table = 'quizzes'

class Question(models.Model):
    quiz_id = models.IntegerField(db_index=True)
    text = models.TextField()
    type = models.TextField(blank=True, null=True)
    options = models.JSONField()
    points = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'questions'

class Challenge(models.Model):
    lesson_id = models.IntegerField(db_index=True)
    title = models.TextField()
    description = models.TextField()
    initial_code = models.TextField()
    solution_code = models.TextField(blank=True, null=True)
    test_cases = models.JSONField()
    points = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'challenges'

class UserProgress(models.Model):
    user_id = models.TextField() # Points to UUID in users table (legacy)
    lesson_id = models.IntegerField(db_index=True)
    completed = models.BooleanField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    last_code = models.TextField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'user_progress'

# --- End Content Models ---

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255, db_index=True)
    mastery = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now_add=True)

class UserMastery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module_id = models.IntegerField()
    mastery_score = models.FloatField(default=0)
    last_source = models.CharField(max_length=50, default="diagnostic")
    last_updated = models.DateTimeField(auto_now=True)

class DiagnosticAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_id = models.IntegerField()
    module_scores = models.JSONField(default=dict)
    overall_score = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class DiagnosticQuestionMeta(models.Model):
    question_id = models.IntegerField(unique=True)
    module_tag = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=50)

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Badge(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.CharField(max_length=255)
    pdf_path = models.CharField(max_length=255)
    issued_at = models.DateTimeField(auto_now_add=True)

class CertificateTemplate(models.Model):
    code = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
