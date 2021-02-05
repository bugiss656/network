from django.db import models
from django.contrib.auth.models import User



class UserFollows(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    following_user = models.CharField(default='', max_length=256)

    def __str__(self):
        return f'{self.user} following users'


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    body = models.CharField(default='', max_length=256)
    post_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    @property
    def post_likes(self):
        return self.likes.all().count()

    @property
    def users(self):
        users = [user['user__username'] for user in self.likes.values('user__username')]
        return users


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='likes')
