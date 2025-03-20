from django.shortcuts import render
from . models import Tweet
from . forms import TweetForm , UserRegistrationForm
from django.shortcuts import get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
# Create your views here.
def index(request):
    return render(request , 'index.html')

def Tweet_list(request):
    Tweets = Tweet.objects.all().order_by('-created_at')
    return render(request , 'tweet_list.html' , {'Tweets' : Tweets})

@login_required
def tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST , request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    
    return render(request , 'tweet_form.html' , {'form' : form})


def tweet_edit(request , tweet_id):
    tweet = get_object_or_404(Tweet , pk = tweet_id , user = request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST , request.FILES , instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request , 'tweet_form.html' , {'form' : form})


def tweet_delete(request , tweet_id):
    tweet = get_object_or_404(Tweet , pk = tweet_id , user = request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    
    return render(request , 'tweet_confirm_delete.html' , {'tweet' : tweet})


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            login(request , user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(request , 'registration/register.html' , {'form' : form})

@login_required
def retweet(request, tweet_id):
    original_tweet = get_object_or_404(Tweet, id=tweet_id)
    
    if not Tweet.objects.filter(user=request.user, retweet_from=original_tweet).exists():
        Tweet.objects.create(user=request.user, retweet_from=original_tweet)
    
    return redirect('tweet_list')

@login_required
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    
    if request.user in tweet.likes.all():
        tweet.likes.remove(request.user)  # Unlike if already liked
    else:
        tweet.likes.add(request.user)  # Like the tweet
    
    return redirect('tweet_list')