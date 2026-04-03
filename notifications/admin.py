from django.contrib import admin
from .models import Notification

# Register your models here.


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    model = Notification

    list_display = ['sender', 'receiver',
                    'notification_type', 'text', 'is_read', 'created_at']
