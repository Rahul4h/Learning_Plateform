from rest_framework import serializers

from .models import ConceptLink, TopicResource


class ConceptLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConceptLink
        fields = [
            "id",
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
        ]


class TopicResourceSerializer(serializers.ModelSerializer):
    concept_links = ConceptLinkSerializer(many=True, read_only=True)

    class Meta:
        model = TopicResource
        fields = [
            "id",
            "title",
            "resource_type",
            "text_content",
            "file_url",
            "youtube_url",
            "thumbnail_url",
            "sort_order",
            "is_featured",
            "concept_links",
        ]
