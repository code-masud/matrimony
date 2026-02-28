from django.urls import path
from .views import *

app_name='notifications'
urlpatterns = [
    path('', NotificationView.as_view(), name='my_notification'),
]
