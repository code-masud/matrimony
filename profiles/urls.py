from django.urls import path
from .views import *

app_name='profiles'
urlpatterns = [
    path('detail/<int:pk>/', ProfileDetail.as_view(), name="detail"),
]
