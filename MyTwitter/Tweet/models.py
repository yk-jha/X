from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Tweet(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    text = models.TextField(max_length=240)
    photo = models.ImageField(upload_to='photos/',blank=True , null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    retweet_from = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='retweets')
    likes = models.ManyToManyField(User, related_name='liked_tweets', blank=True)

    
    def __str__(self):
        return f'{self.user.username} - {self.text}'
    
    def total_likes(self):
        return self.likes.count()
    
    def total_retweets(self):
        return self.retweets.count()