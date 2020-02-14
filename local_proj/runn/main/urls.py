from django.urls import path
# from .views import PostListView
from . import views

urlpatterns = [
    path('', views.home, name="main-home"),
    # path('', PostListView.as_view(), name="main-home"),
    path('about/', views.about, name="main-about"),
]