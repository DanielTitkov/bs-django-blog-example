from django.urls import path
from .views import HomeView, PostDetailView, CreateCommentView, UpdateCommentView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('post/<int:pk>', PostDetailView.as_view(), name="post-details"),
    path('post/<int:pk>/comment', CreateCommentView.as_view(), name="create-comment"),
    path('post/<int:pk>/comment/<int:comment_pk>', UpdateCommentView.as_view(), name="update-comment"),
]

