from django.db import models

from apps.common.constants import SectionType


class TopicSection(models.Model):
    topic = models.ForeignKey(
        "topics.Topic",
        on_delete=models.CASCADE,
        related_name="sections",
    )
    section_type = models.CharField(max_length=40, choices=SectionType.choices)
    title = models.CharField(max_length=255)
    content = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "id"]
        indexes = [
            models.Index(fields=["topic", "section_type", "sort_order"]),
            models.Index(fields=["topic", "sort_order"]),
        ]

    def __str__(self):
        return f"{self.topic.title} - {self.title}"
