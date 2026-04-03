from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from cities_light.models import Country
from django.db.models import Q
from datetime import date, timedelta
from matches.models import InterestRequest, Shortlist
from django.db.models import OuterRef, Exists


User = get_user_model()


class ExploreView(TemplateView):
    template_name = 'explore/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request

        interest_subquery = InterestRequest.objects.filter(
            sender=request.user,
            receiver=OuterRef('pk')
        )

        shortlist_subquery = Shortlist.objects.filter(
            user=request.user,
            shortlisted_user=OuterRef('pk')
        )

        results = User.objects.exclude(
            id=request.user.id
        ).select_related('matrimony_profile').annotate(
            interest_requested=Exists(interest_subquery),
            shortlisted=Exists(shortlist_subquery),
        )

        query = request.GET.get('q', "")
        religion = request.GET.get('religion', "")
        location = request.GET.get('location', "")
        age_range = request.GET.get('age_range', "")

        # 3. Apply Filters
        if query:
            results = results.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )

        if religion:
            results = results.filter(matrimony_profile__religion=religion)

        if location:
            results = results.filter(matrimony_profile__country_id=location)

        if age_range:

            try:
                min_age, max_age = map(int, age_range.split('-'))
                today = date.today()

                results = results.filter(
                    matrimony_profile__date_of_birth__range=[
                        today - timedelta(days=365.25 * max_age),
                        today - timedelta(days=365.25 * min_age)
                    ]
                )
            except ValueError:
                pass

        context["query"] = query
        context["age_range"] = age_range
        context["location"] = location
        context["religion"] = religion
        context["title"] = 'Search'
        context['countries'] = Country.objects.all()
        context['search_result'] = results
        return context
