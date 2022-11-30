import json
from twitter import twitterScript,twitterscripttest
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room

class ChatConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self,event):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        if self.room_name in Room.number.keys():
            Room.number[self.room_name] = Room.number[self.room_name]+ 1
        else:
            Room.number.update({self.room_name:1})    
        if Room.number[self.room_name] == 1:
            if self.room_name in Room.checkin.keys():
                if Room.checkin[self.room_name]:
                    pass
                else:
                    TwitterConnect.foo(self.room_name)
                    Room.checkin.update({self.room_name:True})
            else:
                TwitterConnect.foo(self.room_name)
                Room.checkin.update({self.room_name:True})
            
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print(Room.number[self.room_name])
        if Room.number[self.room_name] == 1:
            if Room.checkin[self.room_name]:
                Room.number[self.room_name] = Room.number[self.room_name] - 1   
        Room.number[self.room_name]  = Room.number[self.room_name]  - 1
        if Room.number[self.room_name] == 0:
            Room.checkin[self.room_name] == False

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
    async def stream(self,event):
        if Room.number[self.room_name] == 1:
            twitterScript.run(self.room_name)
class TwitterConnect(ChatConsumer):
    def foo(argument):
        twitterscripttest.run(argument)
   
   
