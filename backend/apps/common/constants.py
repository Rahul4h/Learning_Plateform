from django.db import models


class ResourceType(models.TextChoices):
    TEXT = "text", "Text"
    AUDIO = "audio", "Audio"
    IMAGE = "image", "Image"
    VIDEO = "video", "Video"
    YOUTUBE = "youtube", "YouTube"


class SectionType(models.TextChoices):
    INTRODUCTION = "introduction", "Introduction"
    DETAILED_EXPLANATION = "detailed_explanation", "Detailed Explanation"
    ADDITIONAL_RESOURCES = "additional_resources", "Additional Resources"
