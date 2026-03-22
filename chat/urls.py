from django.urls import path
from .views import *

app_name='chat'
urlpatterns = [
    path('', ChatView.as_view(), name="my_chat"),
    path('private/<int:pk>', PrivateChat.as_view(), name="private_chat"),
]
