from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import (
	PostListView,
	PostDetailView,
	PostCreateView,
	PostUpdateView,
	PostDeleteView,
    ProfileDetailView,
    ProfileFollowToggle,
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name="main-home"),
    path('admin/', admin.site.urls),
    path('register/', views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name="login"), #temp_name path might be wrong
    path('logout/', auth_views.LogoutView.as_view(template_name='main/logout.html'), name="logout"),
    #path('profile/<int:pk>/', views.profile, name="user-profile"),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name="user-profile"),
    path('profile/<int:pk>/update', views.update_profile, name="update-profile"),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', login_required(PostCreateView.as_view()), name='post-create'),
    path('post/<int:pk>/update/', login_required(PostUpdateView.as_view()), name='post-update'),
    path('post/<int:pk>/delete/', login_required(PostDeleteView.as_view()), name='post-delete'),
    path('profile/<int:pk>/profile-follow/', login_required(ProfileFollowToggle.as_view()), name='follow'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('search/', views.search, name="main-search"),
    path('search_users_name/', views.search_users_name, name="main-search-users-name"),
    path('search_users_location/', views.search_users_location, name="main-search-users-location"),
]
