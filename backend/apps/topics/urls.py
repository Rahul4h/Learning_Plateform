from django.urls import path

from .views import TopicDetailAPIView, TopicListAPIView


urlpatterns = [
    path("", TopicListAPIView.as_view(), name="topic-list"),
    path("<int:id>/", TopicDetailAPIView.as_view(), name="topic-detail"),
]
