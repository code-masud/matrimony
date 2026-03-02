from django.urls import path
from .views import *

app_name='accounts'
urlpatterns = [
    path('user/<int:pk>/update/', UpdateUser.as_view(), name="update_user"),
    path('profile/', MyProfile.as_view(), name="my_profile"),
]
