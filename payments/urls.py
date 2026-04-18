from django.urls import path
from .views import *

app_name = 'payments'
urlpatterns = [
    path('', PaymentView.as_view(), name='my_payment'),
    path('checkout/<int:id>', CheckoutView.as_view(), name='checkout'),
    path('process/<int:id>', process_payment, name='process_payment'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
]
    