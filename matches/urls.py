from django.urls import path
from .views import *


app_name='matches'
urlpatterns = [
    path('', MatchesView.as_view(), name='matches')
]
