from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.
class MyProfile(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'accounts/index.html'
    permission_required = ['accounts.view_user']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'My Profile'
        return context