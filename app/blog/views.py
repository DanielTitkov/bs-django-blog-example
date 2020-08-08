from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Post, Comment
from .forms import CommentForm


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
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs.get('pk')
        return super().form_valid(form)


class UpdateCommentView(UpdateView):
    model = Comment
    template_name = "update-comment.html"
    fields = ('name', 'body')
    pk_url_kwarg = 'comment_pk' 