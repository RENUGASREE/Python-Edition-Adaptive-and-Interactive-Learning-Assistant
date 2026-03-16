from django.contrib import admin
from .models import SkillGapAnalysis, LearningPlan

@admin.register(SkillGapAnalysis)
class SkillGapAnalysisAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'accuracy_percent', 'status', 'last_updated')
    list_filter = ('status', 'last_updated', 'user')
    search_fields = ('user__username', 'topic')
    raw_id_fields = ('user',)

    def accuracy_percent(self, obj):
        return f"{round(obj.accuracy * 100, 1)}%"
    accuracy_percent.short_description = 'Accuracy'
    accuracy_percent.admin_order_field = 'accuracy'

@admin.register(LearningPlan)
class LearningPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'generated_at', 'modules_count', 'lessons_count', 'reasoning_summary')
    list_filter = ('generated_at', 'user')
    search_fields = ('user__username', 'reasoning')
    raw_id_fields = ('user',)
    readonly_fields = ('generated_at',)

    def modules_count(self, obj):
        return len(obj.recommended_modules) if obj.recommended_modules else 0
    modules_count.short_description = 'Modules'

    def lessons_count(self, obj):
        return len(obj.recommended_lessons) if obj.recommended_lessons else 0
    lessons_count.short_description = 'Lessons'

    def reasoning_summary(self, obj):
        if not obj.reasoning:
            return ""
        return obj.reasoning[:75] + "..." if len(obj.reasoning) > 75 else obj.reasoning
    reasoning_summary.short_description = 'Reasoning'