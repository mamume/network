from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self')


class Post(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="liked_posts")

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    owner = models.ManyToManyField(User)
    post = models.ManyToManyField(Post)

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
