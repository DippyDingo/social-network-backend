from rest_framework import serializers

from .geocoding import geocode_location, reverse_location
from .models import Comment, Post, PostImage


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "author", "text", "created_at")
        read_only_fields = ("id", "author", "created_at")


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ("id", "image", "created_at")
        read_only_fields = ("id", "created_at")


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    images = PostImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
        allow_empty=False,
    )
    likes_count = serializers.SerializerMethodField()
    location = serializers.CharField(write_only=True, required=False, allow_blank=True)
    location_name = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "text",
            "image",
            "images",
            "uploaded_images",
            "location",
            "latitude",
            "longitude",
            "location_name",
            "created_at",
            "comments",
            "likes_count",
        )
        read_only_fields = (
            "id",
            "author",
            "images",
            "latitude",
            "longitude",
            "location_name",
            "created_at",
            "comments",
            "likes_count",
        )

    def validate(self, attrs):
        location = attrs.pop("location", None)
        if location is not None:
            location = location.strip()
            if location:
                latitude, longitude = geocode_location(location)
                if latitude is None or longitude is None:
                    raise serializers.ValidationError(
                        {"location": "Не удалось определить координаты для указанной локации."}
                    )
                attrs["location_query"] = location
                attrs["latitude"] = latitude
                attrs["longitude"] = longitude
            else:
                attrs["location_query"] = ""
                attrs["latitude"] = None
                attrs["longitude"] = None

        if self.instance is None:
            main_image = attrs.get("image")
            extra_images = attrs.get("uploaded_images") or []
            if main_image is None and not extra_images:
                raise serializers.ValidationError(
                    {"image": "Загрузите минимум одно изображение для публикации."}
                )

        return attrs

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", [])
        post = super().create(validated_data)
        self._create_extra_images(post, uploaded_images)
        return post

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", [])
        post = super().update(instance, validated_data)
        self._create_extra_images(post, uploaded_images)
        return post

    def _create_extra_images(self, post, uploaded_images):
        if uploaded_images:
            PostImage.objects.bulk_create(
                [PostImage(post=post, image=image) for image in uploaded_images]
            )

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_location_name(self, obj):
        return reverse_location(obj.latitude, obj.longitude)
