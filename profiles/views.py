from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.
class ProfileView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'profile/index.html'
    permission_required = ['profile.view_matrimony_profile']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Profile'
        return context

class ChatView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'profile/chat.html'
    permission_required = ['profile.view_matrimony_profile']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Chat'
        return context
    