from django.shortcuts import render
from django.views.generic import TemplateView
from .utils import send_notification


class NotificationView(TemplateView):
    template_name = 'notifications/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Notifications'
        send_notification(self.request.user.username, 3, "Hello from Django!")
        return context
