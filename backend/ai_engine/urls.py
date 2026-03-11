from django.urls import path
from .views import AiTutorView


urlpatterns = [
    path("ai-tutor", AiTutorView.as_view(), name="ai_tutor"),
]
