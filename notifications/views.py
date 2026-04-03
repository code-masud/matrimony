from django.shortcuts import render
from django.views.generic import TemplateView
from .utils import send_notification
from .models import Notification
from django.http import JsonResponse
from django.views.decorators.http import require_POST


class NotificationView(TemplateView):
    template_name = 'notifications/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Notifications'
        send_notification(self.request.user.username, 3, "Hello from Django!")
        return context


def notification_count(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(
            receiver=request.user,
            is_read=False
        ).count()
    else:
        count = 0

    return JsonResponse({
        "count": count
    })


def unread_notifications(request):
    if not request.user.is_authenticated:
        return JsonResponse({"notifications": []})

    notifications = Notification.objects.filter(
        receiver=request.user,
        is_read=False
    ).order_by('-created_at')[:10]

    data = [
        {
            "id": n.id,
            "text": n.text,
            "sender": n.sender.username,
            "created_at": n.created_at.strftime("%Y-%m-%d %H:%M")
        }
        for n in notifications
    ]

    return JsonResponse({"notifications": data})


@require_POST
def mark_notifications_read(request):
    if request.user.is_authenticated:
        Notification.objects.filter(
            receiver=request.user,
            is_read=False
        ).update(is_read=True)

    return JsonResponse({"status": "ok"})
