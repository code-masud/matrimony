import json

from django.dispatch import receiver
import channels
import redis

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist
from .models import Message

User = get_user_model()

redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

class PresenceConsumer(AsyncWebsocketConsumer):
    GROUP_NAME = 'online_users'
    ONLINE_SET_KEY = "online_users_set"

    async def connect(self):
        self.user = self.scope['user']

        await self.add_user()

        await self.channel_layer.group_add(self.GROUP_NAME, self.channel_name)

        await self.accept()

        await self.channel_layer.group_send(self.GROUP_NAME, {
            'type': 'presence_broadcast',
            'user': self.user.id,
            "status": "online"
        })

    async def disconnect(self, close_code):
        await self.remove_user()

        await self.channel_layer.group_discard(self.GROUP_NAME, self.channel_name)

        await self.channel_layer.group_send(self.GROUP_NAME, {
            'type': 'presence_broadcast',
            'user': self.scope['user'].id,
            "status": "offline"
        })

    async def presence_broadcast(self, event):
        await self.send(text_data=json.dumps(event))

    
    @sync_to_async
    def add_user(self):
        redis_client.sadd(self.ONLINE_SET_KEY, self.scope['user'].id)

    @sync_to_async
    def remove_user(self):
        return redis_client.srem(self.ONLINE_SET_KEY, self.scope['user'].id)
    
    @sync_to_async
    def check_online(self):
        return redis_client.sismember(self.ONLINE_SET_KEY, self.scope['user'].id)

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']
        self.other_username = self.scope["url_route"]["kwargs"]['username']

        if isinstance(self.user, AnonymousUser):
            await self.close(code=4001)
            return
        
        self.other = await self.get_user(self.other_username)

        if not self.other:
            await self.close(code=4001)
            return

        users = sorted([self.user.username, self.other_username])
        self.room_name = f'{users[0]}_{users[1]}'
        self.group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        msg = await self.save_message(message)

        await self.channel_layer.group_send(self.group_name, {
            'type': "chat.message",
            "message": msg.content,
            "sender": self.user.username,
        })

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except ObjectDoesNotExist:
            return None
        
    @sync_to_async
    def save_message(self, message):
        return Message.objects.create(
            sender=self.user,
            receiver=self.other,
            content=message
        )