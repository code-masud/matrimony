from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from datetime import timedelta
from membership.models import Membership, Subscription


class PaymentView(TemplateView):
    template_name = 'payments/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Payment'
        return context


class CheckoutView(TemplateView):
    template_name = 'payments/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['membership'] = Membership.objects.get(id=self.kwargs['id'])
        context["title"] = 'Checkout'
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
