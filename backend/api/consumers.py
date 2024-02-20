import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class Chatconsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.dm_id = self.scope['url_route']['kwargs']['dm']
        self.room_group_name = f'dm_{self.dm_id}'
        #print(self)
        async_to_sync(self.channel_layer.group_add)(self.room_group_name,
                                                    self.channel_name)
        self.send(text_data=json.dumps({
            'type': 'connection established',
            'message': f'dm {self.dm_id} connected',
            'online':True,
        }))

    def disconnect(self, code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']
        async_to_sync(self.channel_layer.group_send)(self.room_group_name,{
            'type':'message',
            'user':user,
            'message':message
        })
    def message(self, event):
        message = event['message']
        user = event['user']
        if type(message) == bool:
            self.send(text_data=json.dumps({
                'type':'online_offline',
                'dm':self.dm_id,
                'user':user,
                'message':message
            }))
        elif type(message) == dict:
            self.send(text_data=json.dumps({
                'type':'dm_message',
                'dm':self.dm_id,
                'user':user,
                'message':message
            }))



class Newchatconsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.user = self.scope['url_route']['kwargs']['user']
        self.room_group_name = f'new_{self.user}'
        async_to_sync(self.channel_layer.group_add)(self.room_group_name,
                                                    self.channel_name)
        self.send(text_data=json.dumps({
            'type': 'connection established',
            'message': f'new {self.user} can now receive new incoming messages',
        }))
    def disconnect(self, code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']
        async_to_sync(self.channel_layer.group_send)(self.room_group_name,{
            'type':'message',
            'user':user,
            'message':message
        })
    def message(self, event):
        message = event['message']
        user = event['user']
        self.send(text_data=json.dumps({
            'type':'new_message',
            'user':user,
            'message':message
        }))