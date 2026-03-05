from django.shortcuts import get_object_or_404

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment, Like, Post
from .serializers import CommentSerializer, PostSerializer


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author").prefetch_related(
        "comments__author",
        "images",
        "likes",
    )
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs["post_id"]).select_related(
            "author",
            "post",
        )

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        serializer.save(author=self.request.user, post=post)


class PostLikeAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        _, created = Like.objects.get_or_create(author=request.user, post=post)
        if created:
            return Response({"detail": "Like added."}, status=status.HTTP_201_CREATED)
        return Response({"detail": "Like already exists."}, status=status.HTTP_200_OK)

    def delete(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        deleted, _ = Like.objects.filter(author=request.user, post=post).delete()
        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Like not found."}, status=status.HTTP_404_NOT_FOUND)
