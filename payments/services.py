import requests
import stripe
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect

client = stripe.StripeClient(settings.STRIPE_SECRET_KEY)


def get_base_url():
    if settings.SSLCOMMERZ["SANDBOX"]:
        return "https://sandbox.sslcommerz.com"
    return "https://securepay.sslcommerz.com"


def initiate_ssl_payment(order, request):
    url = f"{get_base_url()}/gwprocess/v4/api.php"

    success_url = request.build_absolute_uri(
        reverse('payments:payment_success'))
    fail_url = request.build_absolute_uri(reverse('payments:payment_fail'))
    cancel_url = request.build_absolute_uri(reverse('payments:payment_cancel'))

    data = {
        'store_id': settings.SSLCOMMERZ["STORE_ID"],
        'store_passwd': settings.SSLCOMMERZ["STORE_PASSWORD"],
        'total_amount': float(order['amount']),
        'currency': 'USD',
        'tran_id': order['transaction_id'],
        'success_url': success_url,
        'fail_url': fail_url,
        'cancel_url': cancel_url,
        'cus_name': order['name'],
        'cus_email': order['email'],
        'cus_add1': order['address'],
        'cus_phone': order['phone'],
        'shipping_method': 'NO',
        'product_name': order['membership'],
        'product_category': 'General',
        'product_profile': 'general'
    }

    response = requests.post(url, data=data)
    return response.json()


def validate_payment(val_id):
    url = f"{get_base_url()}/validator/api/validationserverAPI.php"

    params = {
        "val_id": val_id,
        "store_id": settings.SSLCOMMERZ["STORE_ID"],
        "store_passwd": settings.SSLCOMMERZ["STORE_PASSWORD"],
        "format": "json"
    }

    response = requests.get(url, params=params)
    return response.json()
