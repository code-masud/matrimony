from django.urls import path
from .views import *

app_name = 'payments'
urlpatterns = [
    path('', PaymentView.as_view(), name='my_payment'),
    path('invoice/<int:pk>', InvoiceView.as_view(), name='invoice'),
    path('checkout/<int:id>', CheckoutView.as_view(), name='checkout'),
    path('process/<int:method_id>', process_payment, name='process_payment'),

    path("success/", payment_success, name='payment_success'),
    path("fail/", payment_fail, name="payment_fail"),
    path("cancel/", payment_cancel, name="payment_cancel"),

    path('success-page/<int:pk>/', SuccessView.as_view(), name='success-page'),
    path('cancel-page/<int:pk>/', CancelView.as_view(), name='cancel-page'),
    path('fail-page/<int:pk>/', FailView.as_view(), name='fail-page'),
]
