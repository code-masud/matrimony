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
    template_name = 'payments/terms_conditions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Terms & Conditions'
        return context