from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse

# Create your models here.


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    thumbnail = models.ImageField()
    timestamp = models.DateTimeField(auto_now=True)
    last_update = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField()
    hidden = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("detail", kwargs={'slug': self.slug})

    def get_like_url(self):
        return reverse("like", kwargs={'slug': self.slug})

    @property
    def comments(self):
        return self.comment_set.filter(hidden=False)

    @property
    def get_comment_count(self):
        return self.comment_set.all().count()

    @property
    def get_like_count(self):
        return self.like_set.all().count()

    @property
    def get_view_count(self):
        return self.postview_set.all().count()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    hidden = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
