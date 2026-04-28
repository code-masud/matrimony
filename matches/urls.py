from django.urls import path
from .views import *

app_name = 'matches'
urlpatterns = [
    path('', MatchesView.as_view(), name='my_match'),
    path('interest/', InterestView.as_view(), name='my_interest'),
    path('shortlist/', ShortListView.as_view(), name='my_shortlist'),
    path('send-interest/', send_interest, name='send_interest'),
    path('accept-interest/', accept_interest, name='accept_interest'),
    path('reject-interest/', reject_interest, name='reject_interest'),
    path('make-shortlist/', make_shortlist, name='make_shortlist'),
    path('remove-shortlist/', remove_shortlist, name='remove_shortlist'),
]
