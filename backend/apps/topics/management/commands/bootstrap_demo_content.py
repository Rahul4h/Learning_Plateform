from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.common.constants import ResourceType, SectionType
from apps.resources.models import ConceptLink, TopicResource
from apps.topic_sections.models import TopicSection
from apps.topics.models import Topic


class Command(BaseCommand):
    help = "Create a demo superuser and seed topic content in an idempotent way."

    def handle(self, *args, **options):
        self.bootstrap_superuser()
        self.bootstrap_topics()
        self.stdout.write(self.style.SUCCESS("Bootstrap complete."))

    def bootstrap_superuser(self):
        user_model = get_user_model()
        username = "rahul"
        email = "rahul255gh68@gmail.com"
        password = "12345"

        user, created = user_model.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            user.set_password(password)
            user.save()
        else:
            updated = False
            if user.email != email:
                user.email = email
                updated = True
            if not user.is_staff:
                user.is_staff = True
                updated = True
            if not user.is_superuser:
                user.is_superuser = True
                updated = True
            if updated:
                user.save()

    def bootstrap_topics(self):
        self.seed_dynamic_programming()
        self.seed_graph_traversal()
        self.seed_binary_search()

    def upsert_topic(self, title, short_description):
        topic, _ = Topic.objects.update_or_create(
            slug=title.lower().replace(" ", "-"),
            defaults={
                "title": title,
                "short_description": short_description,
                "is_published": True,
            },
        )
        return topic

    def upsert_resource(self, topic, title, resource_type, **defaults):
        resource, _ = TopicResource.objects.update_or_create(
            topic=topic,
            title=title,
            defaults={"resource_type": resource_type, **defaults},
        )
        return resource

    def upsert_section(self, topic, section_type, title, content, sort_order):
        TopicSection.objects.update_or_create(
            topic=topic,
            title=title,
            defaults={
                "section_type": section_type,
                "content": content,
                "sort_order": sort_order,
            },
        )

    def upsert_concept(self, resource, label, popup_title, popup_text="", popup_audio_url="", popup_video_url="", popup_youtube_url="", popup_image_url=""):
        text = resource.text_content
        start = text.index(label)
        end = start + len(label)
        ConceptLink.objects.update_or_create(
            topic_resource=resource,
            label=label,
            defaults={
                "start_offset": start,
                "end_offset": end,
                "popup_title": popup_title,
                "popup_text": popup_text,
                "popup_audio_url": popup_audio_url,
                "popup_video_url": popup_video_url,
                "popup_youtube_url": popup_youtube_url,
                "popup_image_url": popup_image_url,
                "sort_order": start,
            },
        )

    def seed_dynamic_programming(self):
        topic = self.upsert_topic(
            "Dynamic Programming",
            "Learn Dynamic Programming through notes, audio, diagrams, video, and concept-level explanations.",
        )
        text_content = (
            "Dynamic Programming is an optimization technique for solving problems with overlapping subproblems. "
            "Top Down Approach solves the problem using recursion and memoization. "
            "Bottom Up Approach solves the same problem iteratively with tabulation. "
            "Memoization stores previous answers so repeated states do not need to be recomputed."
        )
        text_resource = self.upsert_resource(
            topic,
            "Dynamic Programming Notes",
            ResourceType.TEXT,
            text_content=text_content,
            file_url="",
            youtube_url="",
            thumbnail_url="",
            sort_order=1,
            is_featured=True,
        )
        self.upsert_resource(
            topic,
            "DP Audio Overview",
            ResourceType.AUDIO,
            text_content="",
            file_url="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
            youtube_url="",
            thumbnail_url="",
            sort_order=2,
            is_featured=False,
        )
        self.upsert_resource(
            topic,
            "DP State Diagram",
            ResourceType.IMAGE,
            text_content="",
            file_url="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80",
            youtube_url="",
            thumbnail_url="",
            sort_order=3,
            is_featured=False,
        )
        self.upsert_resource(
            topic,
            "DP Whiteboard Explanation",
            ResourceType.VIDEO,
            text_content="",
            file_url="https://www.w3schools.com/html/mov_bbb.mp4",
            youtube_url="",
            thumbnail_url="",
            sort_order=4,
            is_featured=False,
        )
        self.upsert_resource(
            topic,
            "Dynamic Programming Full Tutorial",
            ResourceType.YOUTUBE,
            text_content="",
            file_url="",
            youtube_url="https://www.youtube.com/watch?v=M7lc1UVf-VE",
            thumbnail_url="",
            sort_order=5,
            is_featured=False,
        )
        self.upsert_concept(
            text_resource,
            "Top Down Approach",
            "Top Down Approach",
            popup_text="Top Down Approach starts from the main problem, breaks it into smaller recursive calls, and stores solved states with memoization.",
        )
        self.upsert_concept(
            text_resource,
            "Bottom Up Approach",
            "Bottom Up Approach",
            popup_youtube_url="https://www.youtube.com/watch?v=M7lc1UVf-VE",
        )
        self.upsert_concept(
            text_resource,
            "Memoization",
            "Memoization",
            popup_text="Memoization keeps a cache of previously computed results, so repeated subproblems are not solved again.",
            popup_audio_url="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        )
        self.upsert_section(
            topic,
            SectionType.INTRODUCTION,
            "Introduction",
            "Dynamic Programming works best when a problem has overlapping subproblems and optimal substructure.",
            1,
        )
        self.upsert_section(
            topic,
            SectionType.DETAILED_EXPLANATION,
            "Detailed Explanation",
            "Focus on state definition, transition relation, base case, memoization, and tabulation strategy when solving DP problems.",
            2,
        )
        self.upsert_section(
            topic,
            SectionType.ADDITIONAL_RESOURCES,
            "Additional Resources",
            "Practice Fibonacci, 0/1 Knapsack, Longest Common Subsequence, Coin Change, and LIS to strengthen your DP intuition.",
            3,
        )

    def seed_graph_traversal(self):
        topic = self.upsert_topic(
            "Graph Traversal",
            "Explore BFS, DFS, traversal visuals, and extra reference notes for graph problems.",
        )
        text_content = (
            "Graph traversal includes Breadth First Search and Depth First Search. "
            "Breadth First Search explores level by level, while Depth First Search explores deeply before backtracking."
        )
        text_resource = self.upsert_resource(
            topic,
            "Graph Traversal Notes",
            ResourceType.TEXT,
            text_content=text_content,
            file_url="",
            youtube_url="",
            thumbnail_url="",
            sort_order=1,
            is_featured=True,
        )
        self.upsert_resource(
            topic,
            "Graph Traversal YouTube Walkthrough",
            ResourceType.YOUTUBE,
            text_content="",
            file_url="",
            youtube_url="https://www.youtube.com/watch?v=M7lc1UVf-VE",
            thumbnail_url="",
            sort_order=2,
            is_featured=False,
        )
        self.upsert_concept(
            text_resource,
            "Breadth First Search",
            "Breadth First Search",
            popup_text="Breadth First Search uses a queue and visits nodes layer by layer.",
        )
        self.upsert_concept(
            text_resource,
            "Depth First Search",
            "Depth First Search",
            popup_youtube_url="https://www.youtube.com/watch?v=M7lc1UVf-VE",
        )
        self.upsert_section(
            topic,
            SectionType.INTRODUCTION,
            "Introduction",
            "Graph traversal is used to explore nodes and edges in a structured way.",
            1,
        )
        self.upsert_section(
            topic,
            SectionType.ADDITIONAL_RESOURCES,
            "Additional Resources",
            "Try problems on connected components, shortest path intuition, and cycle detection.",
            2,
        )

    def seed_binary_search(self):
        topic = self.upsert_topic(
            "Binary Search",
            "Understand binary search with step-by-step notes, visual explanation, and video guidance.",
        )
        text_content = (
            "Binary Search works on sorted arrays. Mid calculation helps divide the search space. "
            "Lower Bound and Upper Bound are common variations of binary search."
        )
        text_resource = self.upsert_resource(
            topic,
            "Binary Search Notes",
            ResourceType.TEXT,
            text_content=text_content,
            file_url="",
            youtube_url="",
            thumbnail_url="",
            sort_order=1,
            is_featured=True,
        )
        self.upsert_resource(
            topic,
            "Binary Search Audio Overview",
            ResourceType.AUDIO,
            text_content="",
            file_url="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
            youtube_url="",
            thumbnail_url="",
            sort_order=2,
            is_featured=False,
        )
        self.upsert_resource(
            topic,
            "Binary Search Tutorial",
            ResourceType.YOUTUBE,
            text_content="",
            file_url="",
            youtube_url="https://www.youtube.com/watch?v=M7lc1UVf-VE",
            thumbnail_url="",
            sort_order=3,
            is_featured=False,
        )
        self.upsert_concept(
            text_resource,
            "Mid calculation",
            "Mid calculation",
            popup_text="Mid is usually computed as low + (high - low) // 2 to avoid overflow in some languages.",
        )
        self.upsert_concept(
            text_resource,
            "Lower Bound",
            "Lower Bound",
            popup_youtube_url="https://www.youtube.com/watch?v=M7lc1UVf-VE",
        )
        self.upsert_concept(
            text_resource,
            "Upper Bound",
            "Upper Bound",
            popup_text="Upper Bound finds the first position strictly greater than the target in a sorted array.",
        )
        self.upsert_section(
            topic,
            SectionType.INTRODUCTION,
            "Introduction",
            "Binary Search reduces the search range by half on every step, which gives logarithmic time complexity.",
            1,
        )
        self.upsert_section(
            topic,
            SectionType.DETAILED_EXPLANATION,
            "Detailed Explanation",
            "You need a sorted search space, correct loop conditions, and careful mid updates for left and right boundaries.",
            2,
        )
        self.upsert_section(
            topic,
            SectionType.ADDITIONAL_RESOURCES,
            "Additional Resources",
            "Practice classic binary search, lower bound, upper bound, answer-space binary search, and peak problems.",
            3,
        )
