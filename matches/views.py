from email import message
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import OuterRef, Exists
from django.http import JsonResponse
from .models import InterestRequest, Shortlist
from notifications.models import Notification
from membership.models import Subscription

User = get_user_model()

# Create your views here.


class MatchesView(TemplateView):
    template_name = 'matches/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Matches'
        return context


class InterestView(ListView):
    template_name = 'matches/interest.html'
    context_object_name = 'interests'
    paginate_by = 6

    def get_queryset(self):
        shortlist_subquery = Shortlist.objects.filter(
            user=self.request.user,
            shortlisted_user=OuterRef("receiver")
        )
        return (
            InterestRequest.objects
            .filter(sender=self.request.user)
            .select_related('receiver__matrimony_profile')
            .annotate(has_shortlist=Exists(shortlist_subquery))
            .order_by('-created_at')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Interest'
        return context


class ShortListView(ListView):
    template_name = 'matches/shortlist.html'
    context_object_name = 'shortlists'
    paginate_by = 6

    def get_queryset(self):
        interest_subquery = InterestRequest.objects.filter(
            sender=self.request.user,
            receiver=OuterRef('shortlisted_user')
        )
        return (
            Shortlist.objects
            .filter(user=self.request.user)
            .select_related('shortlisted_user__matrimony_profile')
            .annotate(has_interest=Exists(interest_subquery))
            .order_by('-created_at')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Shortlist'
        return context


@login_required
def send_interest(request):
    receiver_id = request.POST.get('receiver_id')

    if not receiver_id:
        return JsonResponse({"error": "receiver_id missing"}, status=400)

    subscription = (
        Subscription.objects
        .select_related('membership')
        .filter(
            user=request.user,
            is_active=True,
            end_date__gt=timezone.now()
        )
        .first()
    )

    if not subscription or not subscription.can_send_interest():
        return JsonResponse({"error": "Upgrade your plan"}, status=403)

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


@login_required
def make_shortlist(request):
    receiver_id = request.POST.get('receiver_id')

    if not receiver_id:
        return JsonResponse({"error": "receiver_id missing"}, status=400)

    subscription = (
        Subscription.objects
        .select_related('membership')
        .filter(
            user=request.user,
            is_active=True,
            end_date__gt=timezone.now()
        )
        .first()
    )

    if not subscription or not subscription.can_send_interest():
        return JsonResponse({"error": "Upgrade your plan"}, status=403)

    receiver = User.objects.get(id=receiver_id)

    interest, created = Shortlist.objects.get_or_create(
        user=request.user,
        shortlisted_user=receiver,
    )

    if created:
        Notification.objects.create(
            sender=request.user,
            receiver=receiver,
            notification_type="short_list",
            text=f"{request.user.username} short listed you"
        )

        return JsonResponse({
            "status": "success",
            "message": "Shortlisted successfully"
        })

    else:
        return JsonResponse({
            "status": "exists",
            "message": "You already sent shortlist"
        }, status=200)


@login_required
def remove_shortlist(request):
    receiver_id = request.POST.get('receiver_id')

    if not receiver_id:
        return JsonResponse({"error": "receiver_id missing"}, status=400)

    receiver = User.objects.get(id=receiver_id)

    shortlist = Shortlist.objects.get(
        user=request.user,
        shortlisted_user=receiver,
    )

    if shortlist:
        shortlist.delete()

        Notification.objects.create(
            sender=request.user,
            receiver=receiver,
            notification_type="short_list",
            text=f"{request.user.username} remove you from short list"
        )

        return JsonResponse({
            "status": "success",
            "message": "Shortlist remove successfully"
        })

    else:
        return JsonResponse({
            "status": "exists",
            "message": "Shortlist does not exist"
        }, status=200)
