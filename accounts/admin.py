from django.contrib import admin
from .models import Profile, Message, Mission

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "rank",
        "division",
        "status"
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "created_at",
        "is_deleted"
    )

    search_fields = (
        "user__username",
        "content"
    )

    list_filter = (
        "is_deleted",
    )

@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "status",
        "created_at"
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "title",
    )