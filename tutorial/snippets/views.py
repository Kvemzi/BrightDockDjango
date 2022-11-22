
from snippets.models import Twitter

from snippets.serializers import TwitterSerializer
from django.shortcuts import render

from rest_framework import generics

def index(request):
    return render(request, "chat/index.html")
def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

class TwitterList(generics.ListCreateAPIView):
    queryset = Twitter.objects.all()
    serializer_class = TwitterSerializer
class TwitterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Twitter.objects.all()
    serializer_class = TwitterSerializer