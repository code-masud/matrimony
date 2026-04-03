from django.contrib import admin
from .models import InterestRequest

# Register your models here.


@admin.register(InterestRequest)
class InterestRequestAdmin(admin.ModelAdmin):
    model = InterestRequest

    list_display = ['sender', 'receiver',
                    'status', 'message', 'created_at']
