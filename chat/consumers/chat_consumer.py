import json
import redis
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist
from ..models import Message

User = get_user_model()

redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


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

        if text_data_json.get("type") == "typing":
            await self.channel_layer.group_send(self.group_name, {
                "type": "typing.broadcast",
                "user": self.user.username,
            })

        if text_data_json.get("type") == "stop_typing":
            await self.channel_layer.group_send(self.group_name, {
                "type": "stop_typing.broadcast",
                "user": self.user.username,
            })

        if text_data_json.get("type") == "message.delivered":
            msg = await self.get_message(text_data_json.get("message_id"))
            if not msg.is_delivered:
                await self.mark_delivered(text_data_json.get("message_id"))
                await self.channel_layer.group_send(self.group_name, {
                    "type": "message.delivered",
                    "message_id": text_data_json.get("message_id"),
                })

        if text_data_json.get("type") == "message.seen":
            msg = await self.get_message(text_data_json.get("message_id"))
            if not msg.is_seen:
                await self.mark_seen(text_data_json.get("message_id"))
                await self.channel_layer.group_send(self.group_name, {
                    "type": "message.seen",
                    "message_id": text_data_json.get("message_id"),
                })

        if text_data_json.get("type") == "chat.message":
            message = text_data_json.get('message')
            msg = await self.save_message(message)

            await self.channel_layer.group_send(self.group_name, {
                'type': "chat.message",
                "temp_id": text_data_json.get('temp_id'),
                "message_id": msg.id,
                "content": msg.content,
                "sender": self.user.username,
            })

    async def chat_message(self, event):
        await self.mark_delivered(event["message_id"])

        await self.send(text_data=json.dumps(event))

    async def typing_broadcast(self, event):
        if event["user"] != self.user.username:
            await self.send(text_data=json.dumps({
                "type": "typing",
                "user": str(event["user"]).title(),
            }))

    async def stop_typing_broadcast(self, event):
        if event["user"] != self.user.username:
            await self.send(text_data=json.dumps({
                "type": "stop_typing",
                "user": str(event["user"]).title(),
            }))

    async def message_delivered(self, event):
        await self.send(text_data=json.dumps({
            "type": "message.delivered",
            "message_id": event["message_id"],
        }))

    async def message_seen(self, event):
        await self.send(text_data=json.dumps({
            "type": "message.seen",
            "message_id": event["message_id"],
        }))

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

    @sync_to_async
    def get_message(self, message_id):
        return Message.objects.get(id=message_id)

    @sync_to_async
    def mark_delivered(self, message_id):
        return Message.objects.filter(id=message_id).update(is_delivered=True)

    @sync_to_async
    def mark_seen(self, message_id):
        Message.objects.filter(id=message_id).update(
            is_delivered=True, is_seen=True)
