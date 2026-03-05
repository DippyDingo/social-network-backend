from rest_framework import serializers

from .models import Comment, Post


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "author", "text", "created_at")
        read_only_fields = ("id", "author", "created_at")


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "text",
            "image",
            "created_at",
            "comments",
            "likes_count",
        )
        read_only_fields = ("id", "author", "created_at", "comments", "likes_count")

    def get_likes_count(self, obj):
        return obj.likes.count()
