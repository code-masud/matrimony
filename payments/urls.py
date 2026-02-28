from django.urls import path
from .views import *

app_name='payments'
urlpatterns = [
    path('', PaymentView.as_view(), name='my_payment'),
    path('checkout/', PaymentView.as_view(), name='checkout'),
]
