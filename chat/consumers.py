from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatModel,UserProfileModel
from django.contrib.auth.models import User
import json


class PersonalChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        my_id=self.scope['user'].id
        other_user_id=self.scope['url_route']['kwargs']['id']
        if int(my_id)> int(other_user_id):
            self.room_name=f'{my_id}-{other_user_id}'
        else:
            self.room_name=f'{other_user_id}-{my_id}'
        
        self.room_group_name='chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive_json(self, content, **kwargs):
        message =content['message']
        username=content['username']
        timestamp=content['timeStamp']
        print(username)
        print('receive',message)

        await self.save_message(username, self.room_group_name, message )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'username':username,
                'timestamp':timestamp
            }
        )
    async def chat_message(self, event):
        message=event['message']
        username=event['username']
        timestamp=event['timestamp']

        await self.send_json({
            'message':message,
            'username':username,
            'timestamp':timestamp
        })

    @database_sync_to_async
    def save_message(self, username, thread_name, message):
        chat=ChatModel(sender=username, message=message, thread_name=thread_name)
        chat.save()
    
    

    async def disconnect(self,close_code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print('disconnected')



class OnlineStatusConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_group_name='user'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def receive_json(self, content, **kwargs):
        username=content['username']
        connection_type=content['type']
        print(username)
        print(connection_type)
        await self.change_online_status(username, connection_type)

    async def send_onlineStatus(self, event):
        data=json.loads(event.get('value'))
        username=data['username']
        online_status=data['status']
        await self.send_json({
            'username':username,
            'online_status':online_status,
        })
        
    async def disconnect(self, message):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def change_online_status(self,username, c_type):
        user=User.objects.get(username=username)
        userprofile=UserProfileModel.objects.get(user=user)

        if c_type == 'open':
            userprofile.online_status=True
        else:
            userprofile.online_status=False
        userprofile.save()