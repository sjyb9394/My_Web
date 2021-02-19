from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length = 200)
    content = models.TextField()
    author = models.ForeignKey(User,null=True, on_delete=models.CASCADE, related_name='author_post')
    create_date = models.DateTimeField(auto_now=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_post')

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comment')
    create_date = models.DateTimeField(auto_now=True)
    voter = models.ManyToManyField(User, related_name='voter_comment')

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.content


