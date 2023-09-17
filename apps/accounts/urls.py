from django.urls import path
from .views import UserRegistrationView
from . import views


urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('posts/category/<int:category_id>/', views.PostListByCategory.as_view(), name='post-list-by-category'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('communities/', views.CommunityListView.as_view(), name='community-list'),
    path('communities/<int:pk>/', views.CommunityDetailView.as_view(), name='community-detail'),
    path('profile/<int:pk>/', views.ProfileDetail.as_view(), name='user-profile-detail'),
    path('profile/', views.ProfileListAPIView.as_view(), name='profile-list'),
]
