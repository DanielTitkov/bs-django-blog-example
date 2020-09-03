import json
import re
from unidecode import unidecode
from sklearn.feature_extraction.text import CountVectorizer

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt 
from django.http import JsonResponse

from .models import Post, Comment
from .forms import CommentForm



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
    if not post:
        return JsonResponse({"success": False, "message": "post not found"})

    text = post.body
    cleaned_text = unidecode(re.sub('[\W\d\s]', '', text.lower()))
    
    vectorizer = CountVectorizer(
        ngram_range=(3,3),
        lowercase=True,
        analyzer = 'char',
    )

    data = vectorizer.fit_transform([cleaned_text])
    trigrams = vectorizer.get_feature_names()[0:6]

    post.trigrams = " ".join(trigrams)
    post.save()

    return JsonResponse({"success": True, "trigrams": trigrams})