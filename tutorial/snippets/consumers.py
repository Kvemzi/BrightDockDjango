import json
import time
from scripts import tweepyScript
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self,event):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        TwitterConnect.number[self.room_name] = 1
        await self.accept()
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        ) 
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        TwitterConnect.number[self.room_name] -= 1


class TwitterConnect(ChatConsumer):
    number = {}
    checkin = {}
    def check(self, room_name):
        if TwitterConnect.number[room_name] != 0:
            tweepyScript.run()
            time.sleep(5)

   
   
