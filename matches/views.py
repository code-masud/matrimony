from django.db.models import Q, Exists, OuterRef
from django.views.generic import ListView
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
from datetime import date, timedelta
from cities_light.models import Country
from .tasks import send_interest_email, send_shortlist_email

User = get_user_model()

# Create your views here.


class MatchesView(ListView):
    template_name = 'matches/index.html'
    context_object_name = 'matches'
    paginate_by = 6

    def get_queryset(self):
        user = self.request.user
        preference = user.partner_preference

        today = date.today()

        min_dob = date(today.year - preference.max_age, today.month, today.day)
        max_dob = date(today.year - preference.min_age, today.month, today.day)

        queryset = User.objects.select_related('matrimony_profile').filter(
            matrimony_profile__is_profile_completed=True,
            matrimony_profile__date_of_birth__range=(min_dob, max_dob),
        ).exclude(id=user.id)

        filters = Q()

        # if preference.religion:
        #     filters &= Q(matrimony_profile__religion=preference.religion)

        # if preference.marital_status:
        #     filters &= Q(
        #         matrimony_profile__marital_status=preference.marital_status)

        # if preference.education:
        #     filters &= Q(matrimony_profile__education=preference.education)

        # if preference.occupation:
        #     filters &= Q(matrimony_profile__occupation=preference.occupation)

        # if preference.country:
        #     filters &= Q(matrimony_profile__country=preference.country)

        # if preference.state:
        #     filters &= Q(matrimony_profile__state=preference.state)

        # if preference.city:
        #     filters &= Q(matrimony_profile__city=preference.city)

        if preference.min_height_cm:
            filters &= Q(
                matrimony_profile__height_cm__gte=preference.min_height_cm)

        if preference.max_height_cm:
            filters &= Q(
                matrimony_profile__height_cm__lte=preference.max_height_cm)

        queryset = queryset.filter(filters)

        # Filters
        query = self.request.GET.get('q', "")
        religion = self.request.GET.get('religion', "")
        location = self.request.GET.get('location', "")
        age_range = self.request.GET.get('age_range', "")

        if query:
            queryset = queryset.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )

        if religion:
            queryset = queryset.filter(
                matrimony_profile__religion=religion
            )

        if location:
            queryset = queryset.filter(
                matrimony_profile__country_id=location
            )

        if age_range:
            try:
                min_age, max_age = map(int, age_range.split('-'))
                today = date.today()

                queryset = queryset.filter(
                    matrimony_profile__date_of_birth__range=[
                        today - timedelta(days=365.25 * max_age),
                        today - timedelta(days=365.25 * min_age)
                    ]
                )
            except ValueError:
                pass

        interest_subquery = InterestRequest.objects.filter(
            sender=user,
            receiver=OuterRef('pk')
        )

        shortlist_subquery = Shortlist.objects.filter(
            user=user,
            shortlisted_user=OuterRef('pk')
        )

        queryset = queryset.annotate(
            interest_sent=Exists(interest_subquery),
            shortlisted=Exists(shortlist_subquery),
        )

        queryset = queryset.order_by(
            '-matrimony_profile__created_at'
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request

        context["query"] = request.GET.get('q', "")
        context["age_range"] = request.GET.get('age_range', "")
        context["location"] = request.GET.get('location', "")
        context["religion"] = request.GET.get('religion', "")
        context['countries'] = Country.objects.all()

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

        send_interest_email.delay(
            receiver.email,
            "New Interest Received",
            f"{request.user.username} sent you an interest."
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
def accept_interest(request):
    sender_id = request.POST.get('sender_id')

    if not sender_id:
        return JsonResponse({"error": "sender_id missing"}, status=400)

    try:
        interest = InterestRequest.objects.get(
            sender_id=sender_id,
            receiver=request.user,
            status=InterestRequest.StatusChoices.PENDING
        )
    except InterestRequest.DoesNotExist:
        return JsonResponse({"error": "Interest not found"}, status=404)

    interest.status = InterestRequest.StatusChoices.ACCEPTED
    interest.save()

    Notification.objects.create(
        sender=request.user,
        receiver=interest.sender,
        notification_type="interest_accepted",
        text="Your interest was accepted"
    )

    send_interest_email.delay(
        interest.sender.email,
        "Interest Accepted",
        f"{request.user.username} accepted your interest."
    )
    return JsonResponse({"status": "success"})


@login_required
def reject_interest(request):
    sender_id = request.POST.get('sender_id')

    try:
        interest = InterestRequest.objects.get(
            sender_id=sender_id,
            receiver=request.user,
            status=InterestRequest.StatusChoices.PENDING
        )
    except InterestRequest.DoesNotExist:
        return JsonResponse({"error": "Interest not found"}, status=404)

    interest.status = InterestRequest.StatusChoices.REJECTED
    interest.save()

    Notification.objects.create(
        sender=request.user,
        receiver=interest.sender,
        notification_type="interest_rejected",
        text="Your interest was rejected"
    )

    send_interest_email.delay(
        interest.sender.email,
        "Interest Rejected",
        f"{request.user.username} rejected your interest."
    )

    return JsonResponse({"status": "rejected"})


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

        send_shortlist_email.delay(
            receiver.email,
            "Add Shortlist",
            f"{request.user.username} short listed you."
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

        send_shortlist_email.delay(
            receiver.email,
            "Remove Shortlist",
            f"{request.user.username} remove you from short list"
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
