from django.urls import path

from .views import ConceptLinkListAPIView, TopicResourceListAPIView


urlpatterns = [
    path("", TopicResourceListAPIView.as_view(), name="resource-list"),
    path("concept-links/", ConceptLinkListAPIView.as_view(), name="concept-link-list"),
]
