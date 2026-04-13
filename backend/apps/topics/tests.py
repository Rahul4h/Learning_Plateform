from django.test import TestCase

from .models import Topic


class TopicModelTests(TestCase):
    def test_slug_is_generated(self):
        topic = Topic.objects.create(title="Dynamic Programming")
        self.assertEqual(topic.slug, "dynamic-programming")
