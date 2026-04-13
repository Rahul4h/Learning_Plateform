from django.core.exceptions import ValidationError
from django.db import models

from apps.common.constants import ResourceType


class TopicResource(models.Model):
    topic = models.ForeignKey(
        "topics.Topic",
        on_delete=models.CASCADE,
        related_name="resources",
    )
    title = models.CharField(max_length=255)
    resource_type = models.CharField(max_length=20, choices=ResourceType.choices)
    text_content = models.TextField(blank=True)
    file_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    thumbnail_url = models.URLField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["resource_type", "sort_order", "id"]
        indexes = [
            models.Index(fields=["topic", "resource_type", "sort_order"]),
            models.Index(fields=["topic", "is_featured"]),
            models.Index(fields=["created_at"]),
        ]

    def clean(self):
        if self.resource_type == ResourceType.TEXT and not self.text_content:
            raise ValidationError("text_content is required for text resources.")
        if self.resource_type in {ResourceType.AUDIO, ResourceType.IMAGE, ResourceType.VIDEO} and not self.file_url:
            raise ValidationError("file_url is required for audio, image, and video resources.")
        if self.resource_type == ResourceType.YOUTUBE and not self.youtube_url:
            raise ValidationError("youtube_url is required for YouTube resources.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.topic.title} - {self.title}"


class ConceptLink(models.Model):
    topic_resource = models.ForeignKey(
        TopicResource,
        on_delete=models.CASCADE,
        related_name="concept_links",
    )
    label = models.CharField(max_length=255)
    start_offset = models.PositiveIntegerField()
    end_offset = models.PositiveIntegerField()
    popup_title = models.CharField(max_length=255, blank=True)
    popup_text = models.TextField(blank=True)
    popup_audio_url = models.URLField(blank=True)
    popup_video_url = models.URLField(blank=True)
    popup_youtube_url = models.URLField(blank=True)
    popup_image_url = models.URLField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "id"]
        indexes = [
            models.Index(fields=["topic_resource", "sort_order"]),
            models.Index(fields=["topic_resource", "start_offset"]),
        ]

    def clean(self):
        if self.start_offset >= self.end_offset:
            raise ValidationError("start_offset must be less than end_offset.")
        if self.topic_resource_id and self.end_offset > len(self.topic_resource.text_content or ""):
            raise ValidationError("Concept offsets must stay within the text content length.")
        if not any(
            [
                self.popup_text,
                self.popup_audio_url,
                self.popup_video_url,
                self.popup_youtube_url,
                self.popup_image_url,
            ]
        ):
            raise ValidationError("At least one popup content field is required.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.label
