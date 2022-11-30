from django.urls import re_path

from . import consumers
websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.TwitterConnect.as_asgi()),
    re_path(r"ws/twitter/lookups\w+)/$", consumers.ChatConsumer.as_asgi()),

]   