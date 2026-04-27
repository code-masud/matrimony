import stripe
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.utils import timezone
from django.urls import reverse
from django.http import JsonResponse
from datetime import timedelta
from membership.models import Membership, Subscription
from .models import PaymentMethod, Payment
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .utils import generate_trn_id
from .services import initiate_ssl_payment, validate_payment
from django.conf import settings

client = stripe.StripeClient(settings.STRIPE_SECRET_KEY)


class PaymentView(ListView):
    template_name = 'payments/index.html'
    model = Payment
    paginate_by = 5

    def get_object(self):
        return Payment.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Payment'
        return context


class InvoiceView(DetailView):
    template_name = 'payments/invoice.html'
    model = Payment
    context_object_name = 'payment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Invoice"
        return context


class CheckoutView(ListView):
    template_name = 'payments/checkout.html'
    model = PaymentMethod
    context_object_name = 'payment_methods'

    def get_queryset(self):
        return PaymentMethod.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        membership = get_object_or_404(Membership, id=self.kwargs['id'])

        context.update({
            'membership': membership,
            'title': 'Checkout'
        })

        return context


class SuccessView(DetailView):
    template_name = 'payments/success.html'
    model = Payment
    context_object_name = 'payment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Success'
        return context


class CancelView(DetailView):
    template_name = 'payments/cancel.html'
    model = Payment
    context_object_name = 'payment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Cancel'
        return context


class FailView(DetailView):
    template_name = 'payments/fail.html'
    model = Payment
    context_object_name = 'payment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Fail'
        return context


def process_payment(request, method_id):
    if request.method != "POST":
        return redirect("payments:checkout")

    method = get_object_or_404(PaymentMethod, id=method_id, is_active=True)

    membership_id = request.POST.get("membership_id")
    membership = get_object_or_404(Membership, id=membership_id)

    full_name = request.POST.get("full_name")
    email = request.POST.get("email")
    phone = request.POST.get("phone")
    address = request.POST.get("address")

    # Create Payment record
    payment = Payment.objects.create(
        user=request.user,
        name=full_name,
        email=email,
        phone=phone,
        address=address,
        membership=membership,
        amount=membership.price,
        transaction_id=generate_trn_id(),
        payment_method=method,
        status="pending",
        gateway_response={}
    )

    method_name = method.name.lower()

    if method_name == "bkash":
        return redirect("payments:bkash_payment", payment.id)

    elif method_name == "nagad":
        return redirect("payments:nagad_payment", payment.id)

    elif method_name == "stripe":
        try:
            checkout_session = client.v1.checkout.sessions.create(params={
                'line_items': [{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': payment.membership.name,
                        },
                        'unit_amount': int(payment.amount) * 100,
                    },
                    'quantity': 1,
                }],
                'mode': 'payment',
                "success_url": request.build_absolute_uri(
                    reverse("payments:success-page", args=[payment.id])
                ),
                "cancel_url": request.build_absolute_uri(
                    reverse("payments:cancel-page", args=[payment.id])
                ),
            })
        except Exception as e:
            return str(e)

        # Store only necessary info
        payment.status = "completed"

        # Retrieve full session with expanded data
        session = stripe.checkout.Session.retrieve(
            checkout_session.id,
            expand=["payment_intent.charges"]
        )

        # Extract email
        customer_email = None
        if session.customer_details:
            customer_email = session.customer_details.email

        # Extract cardholder name
        cardholder_name = None
        if session.payment_intent and session.payment_intent.charges.data:
            charge = session.payment_intent.charges.data[0]
            cardholder_name = charge.billing_details.name

        # Save data
        payment.gateway_response = {
            "id": session.id,
            "url": session.url,
            "payment_status": session.payment_status,
            "email": customer_email,
            "cardholder_name": cardholder_name,
        }

        # Optional: store directly in fields if you have them
        payment.email = customer_email
        payment.name = cardholder_name

        payment.save()

        handle_successful_payment(payment)

        return redirect(checkout_session.url, code=303)

    elif method_name == "sslcommerz":
        response = initiate_ssl_payment({
            'name': full_name,
            'phone': phone,
            'email': email,
            'address': address,
            'transaction_id': payment.transaction_id,
            'amount': payment.amount,
            'membership': membership.name,
        }, request)

        if response.get("status") == "SUCCESS":
            return redirect(response["GatewayPageURL"])

        return redirect("payments:fail", payment.id)

    return redirect("payments:payment_failed", payment.id)


@csrf_exempt
def payment_success(request):
    val_id = request.POST.get("val_id")
    tran_id = request.POST.get("tran_id")

    payment = get_object_or_404(Payment, transaction_id=tran_id)

    validation = validate_payment(val_id)

    if validation.get("status") == "VALID":
        payment.status = "completed"
        payment.gateway_response = validation
        payment.save()

        handle_successful_payment(payment)

        return redirect("payments:success-page", payment.id)

    payment.status = "failed"
    payment.save()
    return redirect("payments:fail-page", payment.id)


@csrf_exempt
def payment_fail(request):
    tran_id = request.POST.get("tran_id")
    payment = get_object_or_404(Payment, transaction_id=tran_id)

    payment.status = "failed"
    payment.save()

    return redirect("payments:fail-page", payment.id)


@csrf_exempt
def payment_cancel(request):
    tran_id = request.POST.get("tran_id")
    payment = get_object_or_404(Payment, transaction_id=tran_id)

    payment.status = "cancelled"
    payment.save()

    return redirect("payments:cancel-page", payment.id)


def handle_successful_payment(payment):
    if payment.status == 'completed':
        payment.user.subscription_set.filter(
            is_active=True).update(is_active=False)

        Subscription.objects.create(
            user=payment.user,
            membership=payment.membership,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=payment.membership.duration_days),
            is_active=True
        )
