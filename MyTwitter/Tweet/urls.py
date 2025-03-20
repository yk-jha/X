
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('', views.Tweet_list, name='tweet_list'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
    path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),
    path('register/', views.register, name='register'),
    path('<int:tweet_id>/retweet/', views.retweet, name='retweet'),
    path('<int:tweet_id>/like/', views.like_tweet, name='like_tweet'),
]