from django.db import models
from django.conf import settings
from membership.models import Membership


class PaymentMethod(models.Model):
    METHOD_TYPES = [
        ('card', 'Credit/Debit Card'),
        ('mobile_banking', 'Mobile Banking'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
        ('gateway', 'Online Gateway'),
    ]

    name = models.CharField(max_length=100)
    method_type = models.CharField(max_length=50, choices=METHOD_TYPES)

    is_active = models.BooleanField(default=True)

    api_key = models.CharField(max_length=255, blank=True, null=True)
    api_secret = models.CharField(max_length=255, blank=True, null=True)
    config = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=15, null=True)
    email = models.EmailField(max_length=255, null=True)
    address = models.TextField(blank=True, null=True)

    membership = models.ForeignKey(
        Membership, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    transaction_id = models.CharField(max_length=255, unique=True)
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')

    currency = models.CharField(max_length=10, default='BDT')
    gateway_response = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.membership} - {self.amount} ({self.status})"
