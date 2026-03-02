from django.urls import path
from .views import *

app_name='accounts'
urlpatterns = [
    path('profile/', MyProfile.as_view(), name="my_profile"),
]
