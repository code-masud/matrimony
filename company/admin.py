from django.contrib import admin
from .models import CompanyInfo
from django.utils.html import format_html

# Register your models here.
@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    model = CompanyInfo

    list_display = ['logo_preview', 'name', 'phone', 'email', 'address']

    @admin.display(description='Logo')
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src={} style="width:20px; height:20px;">',
                obj.logo.url
            )
        return '---'
    