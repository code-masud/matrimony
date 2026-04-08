from django.contrib import admin
from .models import MatrimonyProfile, PartnerPreference, ProfilePhoto
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(MatrimonyProfile)
class MatrimonyProfileAdmin(admin.ModelAdmin):
    model = MatrimonyProfile

    list_display = (
        'user__username',
        'gender',
        'date_of_birth',
        'height_cm',
        'marital_status',
        'religion',
        'mother_tongue',
        'education',
        'occupation',
        'annual_income',
        'country',
        'is_profile_completed',
    )

    list_display_link = (
        'user__username',
        'gender',
        'date_of_birth',
        'height_cm',
        'marital_status',
        'religion',
        'mother_tongue',
        'education',
        'occupation',
        'annual_income',
        'country',
        'is_profile_completed',
    )
    list_per_page = 10


@admin.register(PartnerPreference)
class PartnerPreferenceAdmin(admin.ModelAdmin):
    model = PartnerPreference
    