from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatModel

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
        print(username)
        print('receive',message)

        await self.save_message(username, self.room_group_name, message )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'username':username,
            }
        )
    async def chat_message(self, event):
        message=event['message']
        username=event['username']

        await self.send_json({
            'message':message,
            'username':username,
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