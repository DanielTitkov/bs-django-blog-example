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