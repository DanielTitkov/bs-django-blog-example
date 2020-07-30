from django.urls import path
from .views import HomeView, PostDetailView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('post/<int:pk>', PostDetailView.as_view(), name="post-details"),
]

