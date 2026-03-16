from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Progress, QuizAttempt, Badge, Certificate, Recommendation, ChatMessage, Module, Lesson, Quiz, Question, Challenge, UserProgress, UserMastery, DiagnosticAttempt, DiagnosticQuestionMeta
from .models import CertificateTemplate

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'level', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('level',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('level',)}),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'mastery', 'last_updated')
    list_filter = ('topic', 'mastery')
    search_fields = ('user__username', 'topic')
    raw_id_fields = ('user',)
    fieldsets = (
        (None, {'fields': ('user', 'topic')}),
        ('Details', {'fields': ('mastery', 'last_updated')}),
    )
    readonly_fields = ('last_updated',)

# @admin.register(QuizAttempt)
# class QuizAttemptAdmin(admin.ModelAdmin):
#     list_display = ('user', 'score', 'total_questions', 'completed_at')
#     list_filter = ('completed_at',)
#     search_fields = ('user__username',)
#     raw_id_fields = ('user', 'quiz')

# @admin.register(QuestionAttempt)
# class QuestionAttemptAdmin(admin.ModelAdmin):
#     list_display = ('attempt', 'question', 'selected_option', 'is_correct')
#     list_filter = ('is_correct',)
#     search_fields = ('attempt__user__username', 'question__text')
#     raw_id_fields = ('attempt', 'question')

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)
    search_fields = ('name', 'description')
    fieldsets = (
        (None, {'fields': ('name', 'description')}),
    )

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('user', 'module', 'issued_at')
    list_filter = ('module', 'issued_at')
    search_fields = ('user__username', 'module')
    raw_id_fields = ('user',)
    fieldsets = (
        (None, {'fields': ('user', 'module')}),
        ('Details', {'fields': ('pdf_path', 'issued_at')}),
    )
    readonly_fields = ('issued_at',)

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'content')
    raw_id_fields = ('user',)
    fieldsets = (
        (None, {'fields': ('user', 'content')}),
        ('Timestamps', {'fields': ('created_at',)}),
    )
    readonly_fields = ('created_at',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('user__username', 'message')
    raw_id_fields = ('user',)
    fieldsets = (
        (None, {'fields': ('user', 'message')}),
        ('Timestamps', {'fields': ('timestamp',)}),
    )
    readonly_fields = ('timestamp',)

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_filter = ('order',)
    search_fields = ('title',)
    fieldsets = (
        (None, {'fields': ('title', 'description', 'order', 'image_url')}),
    )

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module_id', 'order', 'difficulty')
    list_filter = ('module_id', 'difficulty')
    search_fields = ('title', 'slug')
    fieldsets = (
        (None, {'fields': ('module_id', 'title', 'slug', 'content')}),
        ('Metadata', {'fields': ('order', 'difficulty', 'duration')}),
    )

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson_id')
    list_filter = ('lesson_id',)
    search_fields = ('title',)
    fieldsets = (
        (None, {'fields': ('lesson_id', 'title')}),
    )

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz_id', 'points')
    list_filter = ('quiz_id',)
    search_fields = ('text',)
    fieldsets = (
        (None, {'fields': ('quiz_id', 'text', 'type', 'options', 'points')}),
    )

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson_id', 'points')
    list_filter = ('lesson_id',)
    search_fields = ('title',)
    fieldsets = (
        (None, {'fields': ('lesson_id', 'title', 'description')}),
        ('Code', {'fields': ('initial_code', 'solution_code', 'test_cases', 'points')}),
    )

@admin.register(UserMastery)
class UserMasteryAdmin(admin.ModelAdmin):
    list_display = ('user', 'module_id', 'mastery_score', 'last_source', 'last_updated')
    list_filter = ('module_id', 'last_source')
    search_fields = ('user__username',)
    raw_id_fields = ('user',)
    fieldsets = (
        (None, {'fields': ('user', 'module_id', 'mastery_score', 'last_source')}),
    )

@admin.register(DiagnosticAttempt)
class DiagnosticAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz_id', 'score_percent', 'created_at')
    list_filter = ('quiz_id', 'created_at', 'user')
    search_fields = ('user__username',)
    raw_id_fields = ('user',)
    fieldsets = (
        (None, {'fields': ('user', 'quiz_id', 'overall_score', 'module_scores')}),
        ('Timestamps', {'fields': ('created_at',)}),
    )
    readonly_fields = ('created_at',)

    def score_percent(self, obj):
        return f"{round(obj.overall_score, 1)}%"
    score_percent.short_description = 'Overall Score'
    score_percent.admin_order_field = 'overall_score'

@admin.register(DiagnosticQuestionMeta)
class DiagnosticQuestionMetaAdmin(admin.ModelAdmin):
    list_display = ('question_id', 'module_tag', 'difficulty')
    list_filter = ('module_tag', 'difficulty')
    search_fields = ('question_id', 'module_tag')
    fieldsets = (
        (None, {'fields': ('question_id', 'module_tag', 'difficulty')}),
    )

@admin.register(CertificateTemplate)
class CertificateTemplateAdmin(admin.ModelAdmin):
    list_display = ('code', 'title')
    search_fields = ('code', 'title')
