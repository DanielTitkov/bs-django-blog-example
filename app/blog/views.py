import json
import logging


from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt 
from django.http import JsonResponse

from .models import Post, Comment
from .forms import CommentForm
from . import services


logger = logging.getLogger(__name__)


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

    post = services.update_post_trigrams(post_id)
    logger.info(f"analysis requested for post {post}")
    if not post:
        return JsonResponse({"success": False, "message": "post not found"})
    return JsonResponse({"success": True, "trigrams": post.trigrams})


@csrf_exempt
def analyze_comment(request):
    comment_id = json.loads(request.body).get("commentId")
    if not comment_id:
        return JsonResponse({"success": False, "message": "provide commentId"})

    comment = services.update_comment_trigrams(comment_id)
    if not comment:
        return JsonResponse({"success": False, "message": "comment not found"})
    return JsonResponse({"success": True, "trigrams": comment.trigrams})