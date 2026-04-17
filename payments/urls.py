from django.urls import path
from .views import *

app_name = 'payments'
urlpatterns = [
    path('', PaymentView.as_view(), name='my_payment'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
]
