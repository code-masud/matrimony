from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView
from django.utils import timezone
from datetime import timedelta
from membership.models import Membership, Subscription
from .models import PaymentMethod, Payment
import uuid
from django.contrib import messages


class PaymentView(TemplateView):
    template_name = 'payments/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Payment'
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


class SuccessView(TemplateView):
    template_name = 'payments/success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Success'
        return context


class CancelView(TemplateView):
    template_name = 'payments/cancel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Cancel'
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

    if method.name.lower() in ["stripe", "card"]:
        if not request.POST.get("card_number"):
            messages.error(request, "Card details are required")
            return redirect("payments:checkout", id=membership.id)

    elif method.name.lower() in ["bkash", "nagad", "rocket"]:
        if not request.POST.get("mobile_number"):
            messages.error(request, "Mobile number is required")
            return redirect("payments:checkout", id=membership.id)

    # Create Payment record
    payment = Payment.objects.create(
        user=request.user,
        membership=membership,
        amount=membership.price,
        transaction_id=str(uuid.uuid4()),
        payment_method=method,
        status="pending",
        gateway_response={}
    )

    # 🔀 Redirect based on method
    method_name = method.name.lower()

    if method_name == "bkash":
        return redirect("payments:bkash_payment", payment.id)

    elif method_name == "nagad":
        return redirect("payments:nagad_payment", payment.id)

    elif method_name == "stripe":
        return redirect("payments:stripe_payment", payment.id)

    elif method_name == "sslcommerz":
        return redirect("payments:sslcommerz_payment", payment.id)

    return redirect("payments:payment_failed", payment.id)


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
