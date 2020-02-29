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
    CommentUpdateView,
    CommentDeleteView,
    SearchResultsView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name="main-home"),
    path('admin/', admin.site.urls),
    path('register/', views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name="login"), #temp_name path might be wrong
    path('logout/', auth_views.LogoutView.as_view(template_name='main/logout.html'), name="logout"),
    path('post/new/', login_required(PostCreateView.as_view()), name='post-create'),
    path('profile/', views.profile, name="profile"),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', login_required(PostUpdateView.as_view()), name='post-update'),
    path('post/<int:pk>/delete/', login_required(PostDeleteView.as_view()), name='post-delete'),
    path('about/', views.about, name="main-about"),
    path('search/', SearchResultsView.as_view(), name="main-search"),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    # path('post/<int:pk>/comment/<int:cpk>/update/', login_required(CommentUpdateView.as_view()), name='comment-update'),
    # path('post/<int:pk>/comment/<int:cpk>/delete/', login_required(CommentDeleteView.as_view()), name='comment-delete'),
    path('comment/<int:pk>/update/', login_required(CommentUpdateView.as_view()), name='comment-update'),
    path('comment/<int:pk>/delete/', login_required(CommentDeleteView.as_view()), name='comment-delete'),
]
