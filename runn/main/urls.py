from django.contrib import admin
from django.urls import path, include
from .views import (
	PostListView,
	PostDetailView,
	PostCreateView,
	PostUpdateView,
	PostDeleteView,
    #SearchResultsView
)
from . import views

urlpatterns = [
    # path('', views.home, name="main-home"),
    path('', PostListView.as_view(), name="main-home"),
    path('admin/', admin.site.urls),
    path('register/', views.register, name="register"),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name="main-about"),
    path('search/', #SearchResultsView.as_view(),
     views.search,name="main-search"),
]
