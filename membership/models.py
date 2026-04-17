from django.db import models
from django.conf import settings
from django.utils import timezone

class Membership(models.Model):
    Membership_CHOICES = [
        ('free', 'Free'),
        ('premium', 'Premium'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    ]

    name = models.CharField(
        max_length=20, choices=Membership_CHOICES, unique=True)
    duration_days = models.IntegerField(default=30)
    price = models.DecimalField(null=True, max_digits=8, decimal_places=2)
    can_send_interest = models.BooleanField(default=False)
    can_chat = models.BooleanField(default=False)
    priority_support = models.BooleanField(default=False)
    personalized_matchmaking = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.get_name_display()


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True)

    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()

    is_active = models.BooleanField(default=True)

    def is_valid(self):
        return self.end_date > timezone.now()

    def __str__(self):
        return f"{self.user} - {self.membership}"