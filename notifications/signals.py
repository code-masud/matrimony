from django.db.models.signals import post_save
from django.dispatch import receiver
from chat.models import Message
from .models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if not created:
        return

    # create notification
    notification = Notification.objects.create(
        sender=instance.sender,
        receiver=instance.receiver,
        notification_type="message"
    )

    # send realtime
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"user_{instance.receiver.id}",
        {
            "type": "notification_broadcast",
            "data": {
                "id": notification.id,
                "sender": instance.sender.username,
                "type": "message",
                "text": f"{instance.sender.username} sent you a message",
            }
        }
    )