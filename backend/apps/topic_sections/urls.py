from django.urls import path

from .views import TopicSectionListAPIView


urlpatterns = [
    path("", TopicSectionListAPIView.as_view(), name="section-list"),
]
