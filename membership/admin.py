from django.contrib import admin
from .models import Membership


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'duration_days',
        'can_send_interest',
        'can_chat',
        'priority_support',
        'personalized_matchmaking',
        'is_active',
    )

    list_filter = ('is_active', 'can_chat', 'priority_support')
    search_fields = ('name',)
    ordering = ('name',)

    list_editable = ('is_active', 'can_chat', 'priority_support')

    fieldsets = (
        ('Membership Info', {
            'fields': ('name', 'price', 'duration_days', 'is_active')
        }),
        ('Features', {
            'fields': (
                'can_send_interest',
                'can_chat',
                'priority_support',
                'personalized_matchmaking',
            )
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('name',)
        return ()
