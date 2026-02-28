from django.contrib import admin
from .models import CompanyInfo, Carousel
from django.utils.html import format_html

# Register your models here.
@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    model = CompanyInfo

    list_display = ['logo_preview', 'name', 'phone', 'email', 'address']
    list_display_links = ['logo_preview', 'name', 'phone', 'email', 'address']

    @admin.display(description='Logo')
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src={} style="width:20px; height:20px;">',
                obj.logo.url
            )
        return '---'

@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    model = Carousel

    list_display = ['image_preview', 'title', 'description']
    list_display_links = ['image_preview', 'title', 'description']

    @admin.display(description='image')
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src={} style="width:100px; height:100px;">',
                obj.image.url
            )
        return '---'
    