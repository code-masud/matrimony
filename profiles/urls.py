from django.urls import path
from .views import *

app_name='profiles'
urlpatterns = [
    path('<int:pk>/', ProfileDetail.as_view(), name="detail"),
]
