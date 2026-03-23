from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received")
    content = models.TextField()
    is_delivered = models.BooleanField(default=False)
    is_seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def room_name(self):
        users = sorted([self.sender.username, self.receiver.username])
        return f"{users[0]}_{users[1]}"
