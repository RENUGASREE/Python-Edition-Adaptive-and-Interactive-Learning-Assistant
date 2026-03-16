from django.urls import path
from .views import RecommendNextView


urlpatterns = [
    path("recommend-next/", RecommendNextView.as_view(), name="recommend_next"),
]
