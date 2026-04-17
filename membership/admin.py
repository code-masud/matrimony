from django.contrib import admin
from .models import Membership, Subscription


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


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'membership',
        'start_date',
        'end_date',
        'is_active',
        'is_valid_now',
    )

    list_filter = (
        'is_active',
        'membership',
        'start_date',
        'end_date',
    )

    search_fields = (
        'user__username',
    )

    ordering = ('-start_date',)

    list_editable = ('is_active',)

    readonly_fields = (
        'user',
        'membership',
        'start_date',
        'end_date',
    )

    def is_valid_now(self, obj):
        return obj.is_valid()
    
    is_valid_now.boolean = True
    is_valid_now.short_description = "Valid"

    def has_add_permission(self, request):
        return False