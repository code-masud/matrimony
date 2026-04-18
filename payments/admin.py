from django.contrib import admin
from .models import Payment, PaymentMethod


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'method_type',
        'is_active',
        'created_at',
    )

    list_filter = (
        'method_type',
        'is_active',
        'created_at',
    )

    search_fields = (
        'name',
        'method_type',
    )

    ordering = ('-created_at',)

    readonly_fields = ('created_at',)

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'method_type', 'is_active')
        }),
        ('API Credentials', {
            'fields': ('api_key', 'api_secret'),
            'classes': ('collapse',),
        }),
        ('Additional Config', {
            'fields': ('config',),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at',),
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'membership',
        'amount',
        'status',
        'payment_method',
        'transaction_id',
        'created_at',
    )

    list_filter = (
        'status',
        'payment_method',
        'created_at',
    )

    search_fields = (
        'user__username',
        'transaction_id',
    )

    ordering = ('-created_at',)

    readonly_fields = (
        'user',
        'membership',
        'amount',
        'transaction_id',
        'payment_method',
        'created_at',
        'updated_at',
    )

    def has_add_permission(self, request):
        return False
