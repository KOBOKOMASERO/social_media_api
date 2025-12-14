from django.urls import path
from .views import RegisterAPIView, LoginAPIView, ProfileAPIView, PublicUserAPIView
from .views import FollowUserAPIView, UnfollowUserAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('users/<str:username>/', PublicUserAPIView.as_view(), name='public-user'),
    path('follow/<int:user_id>/', FollowUserAPIView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserAPIView.as_view(), name='unfollow-user'),
]