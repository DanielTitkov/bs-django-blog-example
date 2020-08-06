from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Comment

# def home(request):
#     return render(request, "home.html", {})

class HomeView(ListView):
    model = Post
    template_name = "home.html"
    ordering = ["-created", "-id"]


class PostDetailView(DetailView):
    model = Post
    template_name = "post.html"


class CreateCommentView(CreateView):
    model = Comment
    template_name = "create-comment.html"
    fields = "__all__"