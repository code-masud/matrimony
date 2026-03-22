from django.dispatch import receiver
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Message

User = get_user_model()


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/room.html'
    # permission_required = ['chat.view_chat']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.exclude(id=self.request.user.id)
        context["title"] = 'Chat'
        context["users"] = users
        return context


class PrivateChat(LoginRequiredMixin, TemplateView):
    template_name = 'chat/window.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        other = get_object_or_404(User, pk=kwargs['pk'])
        context['other'] = other

        messages = Message.objects.filter(
            Q(sender=self.request.user, receiver=other) |
            Q(sender=other, receiver=self.request.user)
        ).order_by("timestamp")
        context['messages'] = messages
        
        return context
