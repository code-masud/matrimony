from django.urls import path
from .views import *

app_name='chat'
urlpatterns = [
    path('', ChatView.as_view(), name="my_chat"),
]
