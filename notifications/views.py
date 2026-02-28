from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class NotificationView(TemplateView):
    template_name = 'notifications/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Notifications'
        return context
    