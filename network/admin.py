from django.contrib import admin
from .models import Comment, User, Post

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
