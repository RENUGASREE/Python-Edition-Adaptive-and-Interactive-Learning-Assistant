from django.contrib import admin
from .models import DiagnosticQuiz, DiagnosticQuestion, DiagnosticOption, DiagnosticQuizAttempt

@admin.register(DiagnosticQuiz)
class DiagnosticQuizAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title",)

class DiagnosticOptionInline(admin.TabularInline):
    model = DiagnosticOption
    extra = 0

@admin.register(DiagnosticQuestion)
class DiagnosticQuestionAdmin(admin.ModelAdmin):
    list_display = ("quiz", "topic", "difficulty", "points")
    list_filter = ("topic", "difficulty")
    search_fields = ("text",)
    inlines = [DiagnosticOptionInline]

@admin.register(DiagnosticQuizAttempt)
class DiagnosticQuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "quiz", "overall_score", "weighted_score", "difficulty_tier", "start_time", "completed_at", "violation_count", "status")
    list_filter = ("difficulty_tier", "status")
    search_fields = ("user__username",)
