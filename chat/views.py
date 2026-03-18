from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.


class ChatView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'chat/room.html'
    permission_required = ['chat.view_chat']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.exclude(id=self.request.user.id)
        context["title"] = 'Chat'
        context["users"] = users
        return context
