from rest_framework import generics

from apps.common.pagination import StandardResultsSetPagination

from .models import TopicSection
from .serializers import TopicSectionSerializer


class TopicSectionListAPIView(generics.ListAPIView):
    serializer_class = TopicSectionSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = TopicSection.objects.select_related("topic").only(
            "id",
            "topic_id",
            "section_type",
            "title",
            "content",
            "sort_order",
            "topic__id",
            "topic__is_published",
        )
        topic_id = self.request.query_params.get("topic_id")
        if topic_id:
            queryset = queryset.filter(topic_id=topic_id, topic__is_published=True)
        return queryset
