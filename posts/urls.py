from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, PostLikeAPIView, PostViewSet

router = DefaultRouter()
router.register("posts", PostViewSet, basename="post")

urlpatterns = [
    path(
        "posts/<int:post_id>/comments/",
        CommentViewSet.as_view({"get": "list", "post": "create"}),
        name="comment-list-create",
    ),
    path(
        "posts/<int:post_id>/comments/<int:pk>/",
        CommentViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
        name="comment-detail",
    ),
    path("posts/<int:post_id>/like/", PostLikeAPIView.as_view(), name="post-like"),
    *router.urls,
]
