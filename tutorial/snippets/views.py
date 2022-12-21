from snippets.models import Twitter
from snippets.serializers import TwitterSerializer
from django.shortcuts import render
from django.http import HttpResponse
from scripts import tweepyScript
from rest_framework import generics


def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    twitter_post = Twitter.objects
    tweepyScript.run(room_name)
    return render(request, "chat/room.html", {"room_name": room_name, 'twitter_post': twitter_post})
    


def simple_function(request):
    print('Simple')
    




def tweets(request, hashtag):
    twitter_post = Twitter.objects.all()
    return render(request, "twitter/tweets.html", {'twitter_post': twitter_post, 'hashtag': hashtag})


class TwitterList(generics.ListCreateAPIView):
    queryset = Twitter.objects.all()
    serializer_class = TwitterSerializer


class TwitterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Twitter.objects.all()
    serializer_class = TwitterSerializer
