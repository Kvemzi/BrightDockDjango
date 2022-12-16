from snippets.models import Twitter
from snippets.serializers import TwitterSerializer
from django.shortcuts import render


from rest_framework import generics


def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    twitter_post = Twitter.objects
    return render(request, "chat/room.html", {"room_name": room_name, 'twitter_post': twitter_post})


def index_tweet(request):
    return render(request, "twitter/indextweets.html")


def tweets(request, hashtag):
    twitter_post = Twitter.objects.all()
    return render(request, "twitter/tweets.html", {'twitter_post': twitter_post, 'hashtag': hashtag})


class TwitterList(generics.ListCreateAPIView):
    queryset = Twitter.objects.all()
    serializer_class = TwitterSerializer


class TwitterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Twitter.objects.all()
    serializer_class = TwitterSerializer
