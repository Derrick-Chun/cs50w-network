from django.contrib import admin
from .models import User, Post, Follow

admin.site.register(User)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "short_content", "timestamp", "likes_count")
    list_select_related = ("author",)

    def short_content(self, obj):
        return obj.content[:50]

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("follower", "following", "created_at")
    list_select_related = ("follower", "following")
