from urllib import request

from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import get_user_model
from matches.models import InterestRequest, Shortlist
from django.db.models import OuterRef, Exists
from .models import ProfileView

User = get_user_model()


class ProfileDetail(DetailView):
    model = User
    template_name = 'profiles/detail.html'

    def get_queryset(self):
        interest_subquery = InterestRequest.objects.filter(
            sender=self.request.user,
            receiver=OuterRef('pk')
        )

        shortlist_subquery = Shortlist.objects.filter(
            user=self.request.user,
            shortlisted_user=OuterRef('pk')
        )
        queryset = User.objects.filter(pk=self.kwargs['pk']).select_related(
            'matrimony_profile',
            'partner_preference',
        ).prefetch_related(
            'photos'
        ).annotate(
            interest_requested=Exists(interest_subquery),
            shortlisted=Exists(shortlist_subquery),
        )
        return queryset

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        viewer = request.user

        if viewer.is_authenticated and viewer != self.object:
            ProfileView.objects.get_or_create(
                viewer=viewer,
                viewed=self.object
            )

        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Detail - {self.object.get_full_name()}"
        return context
