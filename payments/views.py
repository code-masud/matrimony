from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
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