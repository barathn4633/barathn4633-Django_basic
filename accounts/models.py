from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

import uuid

# Create your models here.
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.user)

    

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
class DisLikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    no_of_likes = models.IntegerField(default=0)
    no_of_dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.user
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', default=uuid.uuid4)
    username = models.CharField(max_length=100, default='default_username')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f'{self.username} - {self.text[:50]}'





