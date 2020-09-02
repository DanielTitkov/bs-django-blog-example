# Part 1 - Basic app

Create new django project

`django-admin startproject app`

Go to app directory

`cd app`

Apply DB migrations

`python manage.py makemigrations && python manage.py migrate`

Create admin user

`python manage.py createsuperuser`

Start app to check if it's working

`python manage.py runserver`

go to http://127.0.0.1:8000/admin/

Create new 'blog' app in our project

`python manage.py startapp blog`

Add 'blog' to app/setting.py

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'blog',
]
```

Add blog urls to app/urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]
```

Add path to home views (absent as yet) to blog/urls.py

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
]
```

Add home view function to blog/views.py

```python
from django.shortcuts import render

def home(request):
    return render(request, "home.html", {})
```

Add simple template to blog/templates/home.html

```html
<h1>This is my blog! Whoa!</h1>
<p>Lots and lots of greate content here!</p>
```

Now we can run server and see out homepage. 

Add blogpost model to blog/models.py

```python
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"<Post '{self.title}' by {self.author}>"
```

Register Post model in blog/admin.py

```python
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```

Apply DB migrations (to add blog table to DB)

`python manage.py makemigrations && python manage.py migrate`

Update blog/views.py

```python
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

# def home(request):
#     return render(request, "home.html", {})

class HomeView(ListView):
    model = Post
    template_name = "home.html"
```

Update blog/url.py

```python
from django.urls import path
from .views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
]
```

Update blog/templates/home.html

```html
<h1>This is my blog! Whoa!</h1>
<p>Lots and lots of greate content here!</p>

{% for post in object_list %}
    {{ post.title }}
    <br>
    <i>{{ post.author }}</i>
    <br>
    {{ post.body }}

{% endfor %}
```

# Part 2 - Views and templates

Now we need to create a page (template) for single post. Create blog/templates/post.html

```html
<h1>{{ post.title }}</h1>
<small><i>{{ post.author }}</i></small>
<hr>
<p>{{ post.body }}</p>
```

Add new view to blog/views.py

```python
class PostDetailView(DetailView):
    model = Post
    template_name = "post.html"
```

Modify blog/urls.py (add `PostDetailView`) 

```python
from django.urls import path
from .views import HomeView, PostDetailView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('post/<int:pk>', PostDetailView.as_view(), name="post-details"),
]
```

Modify blog/templates/home.html (add link to post details page)

```html
<h1>This is my blog! Whoa!</h1>
<p>Lots and lots of greate content here!</p>
<hr>
{% for post in object_list %}
    <h3><a href="{% url 'post-details' post.pk %}">{{ post.title }}</a></h3>
    <i>{{ post.author }}</i>
    <br>
    {{ post.body }}
{% endfor %}
```

Now we can run server and post titles on the homepage will become links to post details page.

Add back link to post blog/templates.html

```html
<h1>{{ post.title }}</h1>
<small><i>{{ post.author }}</i></small>
<hr>
<p>{{ post.body }}</p>
<br>
<a href="{% url 'home' %}">Go back</a>
```

We will now use Bootstrap to make site look better
Create blog/templates/base.html and put common code there (we use template from [https://getbootstrap.com/docs/4.5/getting-started/introduction/#starter-template] and modify it for django)

```html
<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css"
            integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
        <title>Hello, world!</title>
    </head>
    <body>
        <div class="container">
            {% block content %}
            {% endblock %}
        </div>
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"
            integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj"
            crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"
            integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo"
            crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js"
            integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI"
            crossorigin="anonymous"></script>
    </body>
</html>
```

Add block content wrapping to blog/templates/home.html

```html
{% extends 'base.html' %}
{% block content %}
    <h1>This is my blog! Whoa!</h1>
    <p>Lots and lots of greate content here!</p>
    <hr>
    {% for post in object_list %}
    <h3><a href="{% url 'post-details' post.pk %}">{{ post.title }}</a></h3>
    <i>{{ post.author }}</i>
    <br>
    {{ post.body }}
    {% endfor %}
{% endblock %}
```

and blog/templates/post.html

```html
{% extends 'base.html' %}
{% block content %}
    <h1>{{ post.title }}</h1>
    <small><i>{{ post.author }}</i></small>
    <hr>
    <p>{{ post.body }}</p>
    <br>
    <a class="btn btn-secondary" href="{% url 'home' %}">Go back</a>
{% endblock %}
```

Add navbar template from bootstrap to the top of <body> tag in blog/templates/base.html

```html
    <...>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <a class="navbar-brand" href="{% url 'home' %}">Blog</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
        
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="#">Link</a>
                    </li>
                </ul>
            </div>
        </nav>
        <...>
```

Add dynamic block inside title tag in blog/templates/base.html 

```html
<...>
    <title>
        {% block title %}
            MY BLOG
        {% endblock %}
    </title>
<...>
```

And to blog/templates/post.html

```html
{% block title %}
    {{ post.title }}
{% endblock %}
```

Now let's try naive post ordering (change view in blog/views.py). This is temporary solution, but it works

```python
class HomeView(ListView):
    model = Post
    template_name = "home.html"
    ordering = ["-id"]
```

Add time fields to blog/models.py

```python
class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
```

Call makemigrations. Select 1 hit enter if prompt about default value

Add post.created field to blog/templates/post.html

```html
<...>
<small><i>{{ post.author }} | {{ post.created }}</i></small>
<...>
```

and blog/templates/home.html

```html
<...>
<i>{{ post.author }} | {{ post.created }}</i>
<...>
```

Update sorting criteria in blog/views.py one again

```python
class HomeView(ListView):
    model = Post
    template_name = "home.html"
    ordering = ["-created", "-id"]
```

# Part 3 - Forms

Let's create comment models im blog/models.py and migrate it before. 

```python
class Comment(models.Model):   
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Comment to '{self.post.title}' by {self.name}>"
```

Add model admin for comments to blog/admin.py

```python
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'name',
        'created',
        'updated',
    )

admin.site.register(Comment, CommentAdmin)
```

Create new file blog/templates/includes/post-comments.html 

```html
{% if post.comments.exists %}
    {% for comment in post.comments.all %}
        <div class="card" style="margin-bottom: 10px;">
            <div class="card-body">
                <h5><b>{{ comment.name }}</b> says:</h5>
                <p>{{ comment.body }}</p>
                <small>{{ comment.updated }}</small>
            </div>
        </div>
    {% endfor %}
    {% else %}
    <p>No comments... :)</p>
{% endif %}
```

And add include for in blog/templates/post.html (inside the content block)

```html
<hr>
<h2>Comments</h2>
{% include "includes/post-comments.html" %} 
```

Add new view to blog/view.py (don't forget imports)

```python
class CreateCommentView(CreateView):
    model = Comment
    template_name = "create-comment.html"
    fields = "__all__"
```

Add new url to blog/urls.py

```python
path('post/<int:pk>/comment', CreateCommentView.as_view(), name="create-comment"),
```

Add new template blog/templates/create-comment.html

```html
{% extends 'base.html' %}

{% block title %}
    Add comment
{% endblock %}

{% block content %}
    <div class="form-group">
        <form method="POST">
        {% csrf_token %}
        {{ form.as_p }}
        <button class="btn btn-primary">Comment!</button>
    </div>
{% endblock %}
```

Add link to create comment page to blog/templates/post.html (to comment section header)

```html
<h2>Comments <a href="{% url 'create-comment' post.pk %}" class="btn btn-primary btn-sm">Add comment</a></h2>
```

Add get_absolute url method for comment model in blog/models.py

```python
from django.urls import reverse

<...>

class Comment(models.Model):   
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Comment to '{self.post.title}' by {self.name}>"

    def get_absolute_url(self):
        return reverse("post-details", kwargs={'pk': self.post.pk})
```

Add form for comment to blog/forms.py

```python
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "body")
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
```

And modify CreateCommentView at blog/views.py (don't forget about imports)

```python
class CreateCommentView(CreateView):
    model = Comment
    template_name = "create-comment.html"
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs.get('pk')
        return super().form_valid(form)
```

Add update comment template to blog/templates/update-comment.html

```html
{% extends 'base.html' %}

{% block title %}
    Edit comment
{% endblock %}

{% block content %}
    <div class="form-group">
        <form method="POST">
        {% csrf_token %}
        {{ form.as_p }}
        <button class="btn btn-primary">Save</button>
    </div>
{% endblock %}
```

Add update view to blog/views.py (don't forget to import UpdateView)

```python
class UpdateCommentView(UpdateView):
    model = Comment
    template_name = "update-comment.html"
    fields = ('name', 'body')
    pk_url_kwarg = 'comment_pk'
```

Also add url for new view in blog/urls.py

```python
path('post/<int:pk>/comment/<int:comment_pk>', UpdateCommentView.as_view(), name="update-comment"),
```

# Part 4 - Authentication

Create new django app with `python manage.py startapp accounts` (where accounts is voluntary app name)

Add new app's name to app/settings.py

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'blog',
    'accounts',
]
```

Add urls to app/urls.py (order is important!)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('account/', include('django.contrib.auth.urls')),
    path('account/', include('accounts.urls')),
]
```

Now to the accounts app. Create accounts/templates/registration/login.html 

```html
{% extends 'base.html' %}

{% block title %}
    Log in
{% endblock %}

{% block content %}
    <h1>Login to Blog</h1>
    <div class="form-group">
        <form method="POST">
        {% csrf_token %}
        {{ form.as_p }}
        <button class="btn btn-primary">Log in</button>
    </div>
{% endblock %}
```

And accounts/templates/registration/register.html 

```html
{% extends 'base.html' %}

{% block title %}
    Register
{% endblock %}

{% block content %}
    <h1>Register in Blog</h1>
    <div class="form-group">
        <form method="POST">
        {% csrf_token %}
        {{ form.as_p }}
        <button class="btn btn-primary">Sign up</button>
    </div>
{% endblock %}
```

Create new view in accounts/views.py

```python
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


class UserRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "register/register.html"
    success_url = reverse_lazy('login')
```

And create accounts/urls.py

```python
from django.urls import path
from .views import UserRegisterView

urlpatterns = [
    path('register', UserRegisterView.as_view(), name="register"),
]
```

And add links to blog/templates/base.html 

```html
<...>
<div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
        {% if user.is_authenticated %}
            <li class="nav-item">
                <a class="nav-link" href="{% url 'logout' %}">Logout</a>
            </li>
        {% else %}
            <li class="nav-item">
                <a class="nav-link" href="{% url 'register' %}">Register</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="{% url 'login' %}">Login</a>
            </li>
        {% endif %}
    </ul>
</div>
<...>
```

Add redirect urls to app/settings.py

```python
LOGIN_REDIRECT_URL = 'home'

LOGOUT_REDIRECT_URL = 'home'
```

Modify blog/templates/post.html

```html
<hr>
{% if user.is_authenticated %}
    <h2>Comments <a href="{% url 'create-comment' post.pk %}" class="btn btn-primary btn-sm">Add comment</a></h2>
{% else %}
    <h2>Login to add comments</h2>
{% endif %}
{% include "includes/post-comments.html" %} 
```

Add login required mixin to your views (parents order is important) at blog/views.py 

```python
<...>
from django.contrib.auth.mixins import LoginRequiredMixin

<...>

class CreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = "create-comment.html"
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs.get('pk')
        return super().form_valid(form)


class UpdateCommentView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = "update-comment.html"
    fields = ('name', 'body')
    pk_url_kwarg = 'comment_pk' 
```

Update blog/templates/includes/post-comments.html 

```html
<div class="card-body">
    <h5><b>{{ comment.name }}</b> says:</h5>
    <p>{{ comment.body }}</p>
    <p><small>{{ comment.updated }}</small></p>
    {% if user.is_authenticated %}
        <a class="card-link" href="{% url 'update-comment' post.pk comment.pk %}">
            Edit comment
        </a>
    {% endif %}
</div>
```

Add author to comment model at blog/models.py and apply migrations

```python
author = models.ForeignKey(User, on_delete=models.CASCADE)
```

Change `name` to `author.username` at blog/templates/includes/post-comments.html

```html
<h5><b>{{ comment.author.username }}</b> says:</h5>
```

And update comment edit link at blog/templates/includes/post-comments.html

```html
{% if user.is_authenticated and comment.author == request.user %}
    <a class="card-link" href="{% url 'update-comment' post.pk comment.pk %}">
        Edit comment
    </a>
{% endif %}
```

And user update to CreateCommentView at blog/view.py

```python
class CreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = "create-comment.html"
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs.get('pk')
        form.instance.author = self.request.user
        return super().form_valid(form)
```

# Part 5 - Deployment

CREATE NEW BRANCH FOR THIS!

Change values in app/settings.py

```python
SECRET_KEY = os.getenv("SECRET_KEY") or "youneverguess"

DEBUG = os.getenv('DEBUG') == 'TRUE'

<...>

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': '127.0.0.1',
        'PORT': os.getenv("DB_PORT") or "5432",
        'USER': os.getenv("DB_USER") or "blog",
        'NAME': os.getenv("DB_NAME") or "blog",
        'PASSWORD' : os.getenv("DB_PASSWORD") or "123",
    }
}
```

And create .env file in the project root (app/). Use secure key and password, this is just an example. Add it to .gitignore.

```
SECRET_KEY=dfrth34f2ryh43fwedfbfdfaf
DB_PORT=5432
DB_USER=blog
DB_NAME=blog
DB_PASSWORD=123456
```

Install python-dotenv with `pipenv install python-dotenv`.
Also install psycopg2 with `pipenv install psycopg2`.
Modify app/settings.py to read oyur .env file.

```python
import os
from dotenv import load_dotenv

load_dotenv()
```

Now we need to connect to postgres and create a database. 

```bash
psql -U postgres

create database blog;

create user blog with encrypted password '123456';

grant all privileges on database blog to blog;

\q
```

Now it is supposed that you have some machine where the project will be deployed. In the example it has the following IP: *165.22.92.72*. On Linux you can just ssh to it, on Windows you may need Putty. 

Update app/settings.py 

```python
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "165.22.92.72"]
```

On your server:

```bash
sudo apt update
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx
pip3 install pipenv
```

Login to postgres and create a database again:

```bash
sudo -u postgres psql

create database blog;

create user blog with encrypted password '123456';

grant all privileges on database blog to blog;

\q
```

Install gunicorn locally with `pipenv install gunicorn, commit and push`

On server: clone project repo `git clone https://github.com/DanielTitkov/bs-django-blog-example.git`
Go to the directory, create virtual env and install all the libs. 

```bash
cd bs-django-blog-example
pipenv --python=3
pipenv sync
```

Create .env with relevant values on your server. 
Make migrations and migrate. 
Run app with the command: `gunicorn --bind 0.0.0.0:8000 app.wsgi`.
You may need to update firewall rules with `sudo ufw allow 8000`.

Let's create systemd file for gunicorn.

`sudo nano /etc/systemd/system/gunicorn.service`

and there:

```
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/root/bs-django-blog-example/app
ExecStart=pipenv run gunicorn --access-logfile - --workers 3 --bind unix:/root/bs-django-blog-example/blog.sock app.wsgi

[Install]
WantedBy=multi-user.target 
```

and run it 

```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

Check if socket is in place. 
You can check gunicorn logs with `sudo journalctl -u gunicorn` or `sudo systemctl status gunicorn`
We can even try to connect to this socket now `curl --unix-socket blog.sock localhost`

Now we need to configure NGINX. Add new server block to Nginx’s sites-available directory

`sudo nano /etc/nginx/sites-available/blog`

```
server {
    listen 80;
    server_name 165.22.92.72;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root /root/bs-django-blog-example/app;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/root/bs-django-blog-example/blog.sock;
    }
}
```

And link it `sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled`. You can test Nginx configurations with `sudo nginx -t`.
If all is ok, restart nginx `sudo systemctl restart nginx`.
Update firewall rules `sudo ufw allow 'Nginx Full'`

Troubleshooting:

Nginx logs: `sudo tail -F /var/log/nginx/error.log`
Check path: `namei -l /root/bs-django-blog-example/blog.sock`
Change rights to /root `chmod 755 /root`

# Part 6 - Django business logic

For the sake of simlicity we will start with part 4 code here, not part 5. 

Add new field to Post model in blog/models.py and perform migrations.

```python
trigrams = models.TextField(blank=True)
```

Update blog/urls.py

```python
from django.urls import path
from .views import HomeView, PostDetailView, CreateCommentView, UpdateCommentView, analyze_post

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('post/<int:pk>', PostDetailView.as_view(), name="post-details"),
    path('post/<int:pk>/comment', CreateCommentView.as_view(), name="create-comment"),
    path('post/<int:pk>/comment/<int:comment_pk>', UpdateCommentView.as_view(), name="update-comment"),
    path('post/analyze', analyze_post, name="analyze-post"),
]
```

And start new view in blog/views.py

```python
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt 
from django.http import JsonResponse
from .models import Post, Comment
from .forms import CommentForm

import json


@csrf_exempt
def analyze_post(request):
    
    post_id = json.loads(request.body).get("postId")
    if not post_id:
        return JsonResponse({"success": False, "message": "provide postId"})

    post = Post.objects.filter(pk=post_id).first()

    print(post)

    return JsonResponse({"success": True})
```