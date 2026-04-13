from rest_framework import generics

from apps.common.pagination import StandardResultsSetPagination

from .models import ConceptLink, TopicResource
from .serializers import ConceptLinkSerializer, TopicResourceSerializer


class TopicResourceListAPIView(generics.ListAPIView):
    serializer_class = TopicResourceSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = TopicResource.objects.select_related("topic").prefetch_related("concept_links").only(
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
            "topic__id",
            "topic__is_published",
        )
        topic_id = self.request.query_params.get("topic_id")
        resource_type = self.request.query_params.get("type")
        if topic_id:
            queryset = queryset.filter(topic_id=topic_id, topic__is_published=True)
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)
        return queryset


class ConceptLinkListAPIView(generics.ListAPIView):
    serializer_class = ConceptLinkSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = ConceptLink.objects.select_related("topic_resource", "topic_resource__topic").only(
            "id",
            "topic_resource_id",
            "label",
            "start_offset",
            "end_offset",
            "popup_title",
            "popup_text",
            "popup_audio_url",
            "popup_video_url",
            "popup_youtube_url",
            "popup_image_url",
            "sort_order",
            "topic_resource__id",
            "topic_resource__topic_id",
            "topic_resource__topic__is_published",
        )
        resource_id = self.request.query_params.get("resource_id")
        if resource_id:
            queryset = queryset.filter(
                topic_resource_id=resource_id,
                topic_resource__topic__is_published=True,
            )
        return queryset
