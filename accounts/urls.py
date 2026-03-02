from django.urls import path
from .views import *

app_name='accounts'
urlpatterns = [
    path('user/<int:pk>/update/', UpdateUser.as_view(), name="update_user"),
    path('profile/', MyProfile.as_view(), name="my_profile"),
    path('profile/create/', CreateMatrimonyProfile.as_view(), name="create_profile"),
    path('profile/<int:pk>/update/', UpdateMatrimonyProfile.as_view(), name="update_profile"),
]
