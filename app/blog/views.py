from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt 
from django.http import JsonResponse
from .models import Post, Comment
from .forms import CommentForm

import json


class HomeView(ListView):
    model = Post
    template_name = "home.html"
    ordering = ["-created", "-id"]


class PostDetailView(DetailView):
    model = Post
    template_name = "post.html"


class CreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = "create-comment.html"
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs.get('pk')
        form.instance.author = self.request.user
        return super().form_valid(form)



class UpdateCommentView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = "update-comment.html"
    fields = ('name', 'body')
    pk_url_kwarg = 'comment_pk' 


@csrf_exempt
def analyze_post(request):
    
    post_id = json.loads(request.body).get("postId")
    if not post_id:
        return JsonResponse({"success": False, "message": "provide postId"})

    post = Post.objects.filter(pk=post_id).first()

    print(post)

    return JsonResponse({"success": True})