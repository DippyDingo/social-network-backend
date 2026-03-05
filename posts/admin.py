from django.contrib import admin

from .models import Comment, Like, Post, PostImage


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1
    fields = ("image", "created_at")
    readonly_fields = ("created_at",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "created_at", "latitude", "longitude")
    search_fields = ("text", "location_query")
    list_filter = ("created_at",)
    inlines = (PostImageInline,)


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "created_at")
    list_filter = ("created_at",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "post", "created_at")
    search_fields = ("text",)
    list_filter = ("created_at",)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "post", "created_at")
    list_filter = ("created_at",)
