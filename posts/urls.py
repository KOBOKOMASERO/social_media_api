from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PostViewSet, CommentViewSet, FeedAPIView, PostViewSet, CommentViewSet, LikePostAPIView, UnlikePostAPIView


router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedAPIView.as_view(), name='user-feed'),
    path('posts/<int:pk>/like/', LikePostAPIView.as_view(), name='like-post'),
    path('posts/<int:pk>/unlike/', UnlikePostAPIView.as_view(), name='unlike-post'),
]
