from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

class ProfileDetail(DetailView):
    model = User
    template_name = 'profiles/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f'Detail - {self.get_object().username}'
        return context
