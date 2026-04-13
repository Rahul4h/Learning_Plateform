from rest_framework import serializers

from apps.resources.serializers import TopicResourceSerializer
from apps.topic_sections.serializers import TopicSectionSerializer

from .models import Topic


class TopicListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ["id", "title", "slug", "short_description"]


class TopicDetailSerializer(serializers.ModelSerializer):
    sections = TopicSectionSerializer(many=True, read_only=True)
    resources = TopicResourceSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = [
            "id",
            "title",
            "slug",
            "short_description",
            "sections",
            "resources",
        ]
