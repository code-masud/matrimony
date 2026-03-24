from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_notification(sender, receiver, message):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f'user_{receiver}', {
            'type': "notification_broadcast",
            "data": {
                "id": 1,
                "sender": sender,
                "type": "message",
                "text": f"{sender} sent you a message",
            }
        }
    )
