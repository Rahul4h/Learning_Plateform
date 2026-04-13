from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from django.views.generic import TemplateView


def api_home(request):
    return JsonResponse(
        {
            "message": "Interactive Learning Platform API",
            "endpoints": {
                "admin": "/admin/",
                "topics": "/api/topics/",
                "resources": "/api/resources/",
                "concept_links": "/api/resources/concept-links/",
                "sections": "/api/sections/",
            },
        }
    )


urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path("api/", api_home, name="api_home"),
    path("admin/", admin.site.urls),
    path("api/topics/", include("apps.topics.urls")),
    path("api/resources/", include("apps.resources.urls")),
    path("api/sections/", include("apps.topic_sections.urls")),
]
