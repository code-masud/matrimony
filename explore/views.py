from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class ExploreView(TemplateView):
    template_name = 'explore/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Search'
        return context