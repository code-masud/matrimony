from django.dispatch import receiver
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Message
from matches.models import InterestRequest

User = get_user_model()


class ChatView(LoginRequiredMixin, ListView):
    template_name = 'chat/room.html'
    # permission_required = ['chat.view_chat']
    context_object_name = 'users'

    def get_queryset(self):
        return InterestRequest.objects.filter(
            sender=self.request.user,
            status=InterestRequest.StatusChoices.ACCEPTED
        ).select_related('receiver__matrimony_profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Chat'
        return context


class PrivateChat(LoginRequiredMixin, TemplateView):
    template_name = 'chat/window.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        other = get_object_or_404(User, pk=kwargs['pk'])
        context['other'] = other

        Message.objects.filter(
            sender=other,
            receiver=self.request.user,
            is_seen=False
        ).update(is_delivered=True, is_seen=True)

        messages = Message.objects.filter(
            Q(sender=self.request.user, receiver=other) |
            Q(sender=other, receiver=self.request.user)
        ).order_by("timestamp")[:10]
        context['messages'] = messages

        return context
