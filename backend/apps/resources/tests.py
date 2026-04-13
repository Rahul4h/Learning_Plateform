from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.common.constants import ResourceType
from apps.topics.models import Topic

from .models import ConceptLink, TopicResource


class TopicResourceModelTests(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(title="Dynamic Programming")

    def test_text_resource_requires_text_content(self):
        resource = TopicResource(
            topic=self.topic,
            title="DP Notes",
            resource_type=ResourceType.TEXT,
        )
        with self.assertRaises(ValidationError):
            resource.full_clean()

    def test_concept_link_requires_popup_content(self):
        resource = TopicResource.objects.create(
            topic=self.topic,
            title="DP Notes",
            resource_type=ResourceType.TEXT,
            text_content="Top down and bottom up are two core approaches.",
        )
        concept = ConceptLink(
            topic_resource=resource,
            label="Top down",
            start_offset=0,
            end_offset=8,
        )
        with self.assertRaises(ValidationError):
            concept.full_clean()
