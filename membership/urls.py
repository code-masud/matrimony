from django.urls import path
from .views import *

app_name='membership'
urlpatterns = [
    path('', MembershipView.as_view(), name='my_membership')
]
