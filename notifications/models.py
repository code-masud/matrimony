from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):

    NOTIFICATION_TYPES = (
        ("interest_sent", "Interest Sent"),
        ("interest_accepted", "Interest Accepted"),
        ("interest_declined", "Interest Declined"),
        ("profile_view", "Profile Viewed"),
        ("short_list", "Short List"),
        ("message", "Message"),
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_notifications"
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    notification_type = models.CharField(
        max_length=50,
        choices=NOTIFICATION_TYPES
    )

    text = models.TextField(blank=True)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.notification_type})"