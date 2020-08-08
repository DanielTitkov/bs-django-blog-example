from django.contrib import admin
from .models import Post, Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'name',
        'created',
        'updated',
    )

admin.site.register(Comment, CommentAdmin)
admin.site.register(Post)