from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'phone',
        'email',
        'on_behalf',
        'is_verified',
        'is_staff',
        'is_active',
        'date_joined',
    )
    list_display_links = ('id', 'username', 'first_name',
                          'last_name', 'phone', 'email')
    list_per_page = 10
    list_filter = (
        'is_verified',
        'is_staff',
        'is_active',
        'on_behalf',
        'date_joined',
    )

    search_fields = (
        'username',
        'phone',
        'email',
    )

    ordering = ('-date_joined',)

    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        (_('Personal Info'), {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        (_('On Behalf Info'), {
            'fields': ('on_behalf',)
        }),
        (_('Verification'), {
            'fields': ('is_verified',)
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
        (_('Important Dates'), {
            'fields': ('last_login', 'date_joined'),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'phone',
                'email',
                'password1',
                'password2',
                'on_behalf',
                'is_verified',
                'is_staff',
                'is_active',
            ),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            if obj.is_staff:
                obj.is_verified = True
        super().save_model(request, obj, form, change)
