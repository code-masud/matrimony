from django.contrib import admin
from .models import Message

# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    model = Message

    list_display = (
        'sender',
        'receiver',
        'content',
        'is_delivered',
        'is_seen',
    )

    list_per_page = 10