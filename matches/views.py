from email import message

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from django.http import JsonResponse
from .models import InterestRequest
from notifications.models import Notification

User = get_user_model()

# Create your views here.


class MatchesView(TemplateView):
    template_name = 'matches/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Matches'
        return context


class ShortListView(TemplateView):
    template_name = 'matches/shortlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Shortlist'
        return context


@login_required
def send_interest(request):
    receiver_id = request.POST.get('receiver_id')

    if not receiver_id:
        return JsonResponse({"error": "receiver_id missing"}, status=400)

    receiver = User.objects.get(id=receiver_id)

    interest, created = InterestRequest.objects.get_or_create(
        sender=request.user,
        receiver=receiver,
        defaults={  
            "status": InterestRequest.StatusChoices.PENDING,
            "message": f"{request.user.username} sent you an interest"
        }
    )

    if created:
        Notification.objects.create(
            sender=request.user,
            receiver=receiver,
            notification_type="interest_sent",
            text=f"{request.user.username} sent you an interest"
        )

        return JsonResponse({
            "status": "success",
            "message": "Interest sent successfully"
        })

    else:
        return JsonResponse({
            "status": "exists",
            "message": "You already sent interest"
        }, status=200)
