from django.contrib import admin

from .models import ConceptLink, TopicResource


@admin.register(TopicResource)
class TopicResourceAdmin(admin.ModelAdmin):
    list_display = ("id", "topic", "title", "resource_type", "sort_order", "is_featured")
    list_filter = ("resource_type", "is_featured")
    search_fields = ("title", "topic__title")


@admin.register(ConceptLink)
class ConceptLinkAdmin(admin.ModelAdmin):
    list_display = ("id", "topic_resource", "label", "sort_order")
    search_fields = ("label", "topic_resource__title", "topic_resource__topic__title")
