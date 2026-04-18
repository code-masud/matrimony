from django.shortcuts import render
from django.views.generic import ListView

from membership.models import Membership


class MembershipView(ListView):
    template_name = 'membership/index.html'
    model = Membership
    context_object_name = 'memberships'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Membership'
        return context
