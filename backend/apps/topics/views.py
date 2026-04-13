from django.db.models import Prefetch, Q
from rest_framework import generics

from apps.common.pagination import StandardResultsSetPagination
from apps.resources.models import TopicResource

from .models import Topic
from .serializers import TopicDetailSerializer, TopicListSerializer


class TopicListAPIView(generics.ListAPIView):
    serializer_class = TopicListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Topic.objects.filter(is_published=True).only(
            "id",
            "title",
            "slug",
            "short_description",
            "is_published",
        )
        query = (self.request.query_params.get("q") or "").strip()
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(short_description__icontains=query)
            )
        return queryset


class TopicDetailAPIView(generics.RetrieveAPIView):
    serializer_class = TopicDetailSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Topic.objects.filter(is_published=True).only(
            "id",
            "title",
            "slug",
            "short_description",
            "is_published",
        ).prefetch_related(
            "sections",
            Prefetch(
                "resources",
                queryset=TopicResource.objects.only(
                    "id",
                    "topic_id",
                    "title",
                    "resource_type",
                    "text_content",
                    "file_url",
                    "youtube_url",
                    "thumbnail_url",
                    "sort_order",
                    "is_featured",
                ).prefetch_related("concept_links"),
            ),
        )
