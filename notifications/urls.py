from django.urls import path
from .views import *

app_name = 'notifications'
urlpatterns = [
    path('', NotificationView.as_view(), name='my_notification'),
    path('count/', notification_count, name='count'),
    path('unread/', unread_notifications, name='unread'),
    path('mark-read/', mark_notifications_read, name='mark_read'),
]
