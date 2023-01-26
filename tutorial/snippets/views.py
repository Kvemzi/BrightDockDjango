from snippets.models import Twitter
from snippets.serializers import TwitterSerializer
from django.shortcuts import render
from django.http import HttpResponse
from scripts import tweepyScript
from rest_framework import generics


def index(request):
    """
    ``Search bar:``
    User's input to search twitters hashtag.
    Returns new room with given tweets from DB

    **Template:**
    :template:chat/index.html`
    """
    return render(request, "chat/index.html")


def room(request, room_name):
    """
    Display last 10 tweets from Twitter serach by users input. Kepps updated until user leaves the site.

    **Context**
    Displaying Twitter instances as a notification. Firtsly before user connects to site it runs the following script: :template:'scripts.tweepyScript.py'
    
    ``Twitter``
        An instance of :model:`snippets.Twitter`.

    **Template:**

    :template:`chat/room.html`
    """
    twitter_post = Twitter.objects
    tweepyScript.run(room_name)
    return render(request, "chat/room.html", {"room_name": room_name, 'twitter_post': twitter_post})
    print('post')


def tweets(request, hashtag):
    twitter_post = Twitter.objects.all()
    return render(request, "twitter/tweets.html", {'twitter_post': twitter_post, 'hashtag': hashtag})


class TwitterList(generics.ListCreateAPIView):
    """
    Display an individual :model:`snippets.Twitter`.

    **Context**
    Displaying Twitter instances as a list 

    ``Twitter``
        An instance of :model:`snippets.Twitter`.

    **Template:**

    :template:`rest_framework`
    """
    queryset = Twitter.objects.all()
    serializer_class = TwitterSerializer


class TwitterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Twitter.objects.all()
    serializer_class = TwitterSerializer
