from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import (
	PostListView,
	PostDetailView,
	PostCreateView,
	PostUpdateView,
	PostDeleteView,
    SearchResultsView
)
from . import views

urlpatterns = [
    # path('', views.home, name="main-home"),
    path('', PostListView.as_view(), name="main-home"),
    path('admin/', admin.site.urls),
    path('register/', views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name="login"), #temp_name path might be wrong
    path('logout/', auth_views.LogoutView.as_view(template_name='main/logout.html'), name="logout"),
    path('profile/', views.profile, name="profile"),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name="main-about"),
    path('search/', SearchResultsView.as_view(), name="main-search"),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
]
