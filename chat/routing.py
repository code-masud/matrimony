from django.urls import re_path
from .consumers import presence_consumer, chat_consumer

websocket_urlpatterns = [
    re_path(r'ws/presence/$', presence_consumer.PresenceConsumer.as_asgi()),
    re_path(r"ws/private/(?P<username>\w+)/$", chat_consumer.ChatConsumer.as_asgi()),
]
