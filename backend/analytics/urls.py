from django.urls import path
from .views import AnalyticsView, SkillGapView, LearningPlanView


urlpatterns = [
    path("skill-gaps/", SkillGapView.as_view(), name="skill_gaps"),
    path("learning-plan/", LearningPlanView.as_view(), name="learning_plan"),
    path("analytics", AnalyticsView.as_view(), name="analytics"),
