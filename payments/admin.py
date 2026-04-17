from django.contrib import admin
from .models import Payment

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