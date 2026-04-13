from rest_framework import serializers

from .models import TopicSection


class TopicSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicSection
        fields = ["id", "section_type", "title", "content", "sort_order"]
