from django.contrib import admin
from .models import SkillGapAnalysis, LearningPlan

@admin.register(SkillGapAnalysis)
class SkillGapAnalysisAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'accuracy', 'status', 'last_updated')
    list_filter = ('status', 'last_updated')
    search_fields = ('user__username', 'topic')
    raw_id_fields = ('user',)

@admin.register(LearningPlan)
class LearningPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'generated_at')
    list_filter = ('generated_at',)
    search_fields = ('user__username',)
    raw_id_fields = ('user',)