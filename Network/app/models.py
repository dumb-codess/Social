import uuid
from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone


# Create your models here.

class post(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created= models.DateTimeField(default=django.utils.timezone.now,auto_created=django.utils.timezone.now)
    class Meta:
        ordering = ['-created']
    def likedCount(self):
        return self.likes.count()
    def __str__(self):
        return f"Post by {self.author.username}"

class profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    following= models.ManyToManyField(User,related_name='following',blank=True )
    
    def followerCount(self):
        return self.followers.count()

    def __str__(self):
        return self.user.username
    
    
class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    created= models.DateTimeField(default=django.utils.timezone.now,auto_created=django.utils.timezone.now)


    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"