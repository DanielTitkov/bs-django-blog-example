## Part 1

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

## Part 2

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