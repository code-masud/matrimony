from django.contrib import admin
from .models import InterestRequest, Shortlist

# Register your models here.


@admin.register(InterestRequest)
class InterestRequestAdmin(admin.ModelAdmin):
    model = InterestRequest

    readonly_fields = ['created_at']
    list_display = ['sender', 'receiver',
                    'status', 'message']


@admin.register(Shortlist)
class ShortlistAdmin(admin.ModelAdmin):
    model = Shortlist

    readonly_fields = ['created_at']
    list_display = ['user',  'shortlisted_user']
