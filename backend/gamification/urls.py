from django.urls import path
from .views import GamificationSummaryView


urlpatterns = [
    path("gamification/summary", GamificationSummaryView.as_view(), name="gamification_summary"),
]
