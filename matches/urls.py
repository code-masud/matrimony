from django.urls import path
from .views import *

app_name='matches'
urlpatterns = [
    path('matches/', MatchesView.as_view(), name='my_match'),
    path('shortlist/', ShortListView.as_view(), name='my_shortlist'),
]
