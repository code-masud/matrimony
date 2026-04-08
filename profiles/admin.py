from django.contrib import admin
from .models import MatrimonyProfile, PartnerPreference, ProfilePhoto
from django.contrib.auth import get_user_model
from django.utils.html import format_html

User = get_user_model()


@admin.register(MatrimonyProfile)
class MatrimonyProfileAdmin(admin.ModelAdmin):
    model = MatrimonyProfile

    list_display = (
        'user__username',
        'show_img',
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

    def show_img(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="80" height="80" style="object-fit: contain;" />', obj.profile_picture.url)
        return "No Image"


@admin.register(PartnerPreference)
class PartnerPreferenceAdmin(admin.ModelAdmin):
    model = PartnerPreference

    list_display = (
        'user__username',
        'min_age',
        'max_age',
        'min_height_cm',
        'max_height_cm',
        'religion',
        'marital_status',
        'education',
        'occupation',
        'country'
    )
    list_display_links = (
        'user__username',
        'min_age',
        'max_age',
        'min_height_cm',
        'max_height_cm',
        'religion',
        'marital_status',
        'education',
        'occupation',
        'country'
    )
    list_per_page = 10


@admin.register(ProfilePhoto)
class ProfilePhotoAdmin(admin.ModelAdmin):

    model = ProfilePhoto
    list_display = (
        'user__username',
        'show_img',
    )
    list_per_page = 10

    def show_img(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="80" style="object-fit: contain;" />', obj.image.url)
        return "No Image"
