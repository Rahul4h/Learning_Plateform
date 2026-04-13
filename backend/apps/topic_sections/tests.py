from django.test import TestCase

from apps.common.constants import SectionType
from apps.topics.models import Topic

from .models import TopicSection


class TopicSectionModelTests(TestCase):
    def test_section_string_representation(self):
        topic = Topic.objects.create(title="DP")
        section = TopicSection.objects.create(
            topic=topic,
            section_type=SectionType.INTRODUCTION,
            title="Introduction",
            content="Intro",
        )
        self.assertEqual(str(section), "DP - Introduction")
