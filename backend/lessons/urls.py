from django.urls import path
from .views import LessonProfileView, LessonByDifficultyView


urlpatterns = [
    path("lessons/<int:lesson_id>/profile", LessonProfileView.as_view(), name="lesson_profile"),
    path("lessons/by-difficulty", LessonByDifficultyView.as_view(), name="lessons_by_difficulty"),
]
