from django.contrib import admin

from .models import TopicSection


@admin.register(TopicSection)
class TopicSectionAdmin(admin.ModelAdmin):
    list_display = ("id", "topic", "section_type", "title", "sort_order")
    list_filter = ("section_type",)
    search_fields = ("title", "topic__title")
