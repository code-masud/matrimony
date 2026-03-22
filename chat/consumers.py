import json
import channels
import redis

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.conf import settings

redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

class PresenceConsumer(AsyncWebsocketConsumer):
    GROUP_NAME = 'online_users'
    ONLINE_SET_KEY = "online_users_set"

    async def connect(self):
        self.user = self.scope['user'].username

        await self.add_user()

        await self.channel_layer.group_add(self.GROUP_NAME, self.channel_name)

        await self.accept()

        await self.channel_layer.group_send(self.GROUP_NAME, {
            'type': 'presence_broadcast',
            'user': self.scope['user'].id,
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