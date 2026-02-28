from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Carousel

# Create your views here.
class HomeView(TemplateView):
    template_name = 'company/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Home'
        context["carousels"] = Carousel.objects.filter(is_active=True).all()
        return context
    