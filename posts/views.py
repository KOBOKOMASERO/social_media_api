from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, filters, status
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from notifications.models import Notification

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Posts CRUD
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        # Optional: restrict update to author only
        if self.request.user != serializer.instance.author:
            raise permissions.PermissionDenied("You cannot edit this post")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise permissions.PermissionDenied("You cannot delete this post")
        instance.delete()

# Comments CRUD
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # Optionally filter comments by post id
        post_id = self.request.query_params.get('post')
        if post_id:
            return Comment.objects.filter(post_id=post_id).order_by('-created_at')
        return Comment.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise permissions.PermissionDenied("You cannot edit this comment")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise permissions.PermissionDenied("You cannot delete this comment")
        instance.delete()

# Feed API
class FeedAPIView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # get posts by users current user follows
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')


class LikePostAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            # create notification
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                target=post
            )
            return Response({'detail': 'Post liked'}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'You already liked this post'}, status=status.HTTP_400_BAD_REQUEST)

class UnlikePostAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post).first()
        if like:
            like.delete()
            return Response({'detail': 'Post unliked'}, status=status.HTTP_200_OK)
        return Response({'detail': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)
