from django.urls import path
from .views import HomeView, PostDetailView, CreateCommentView, UpdateCommentView, analyze_post, analyze_comment

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('post/<int:pk>', PostDetailView.as_view(), name="post-details"),
    path('post/<int:pk>/comment', CreateCommentView.as_view(), name="create-comment"),
    path('post/<int:pk>/comment/<int:comment_pk>', UpdateCommentView.as_view(), name="update-comment"),
    path('post/analyze', analyze_post, name="analyze-post"),
    path('comment/analyze', analyze_comment, name="analyze-comment"),
]

