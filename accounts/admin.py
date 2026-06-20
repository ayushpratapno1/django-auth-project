from django.contrib import admin
from .models import Profile, Message


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