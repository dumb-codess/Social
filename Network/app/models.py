import uuid
from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if instance.is_superuser:
        instance.profile.save()