from django.views.generic import ListView
from django.contrib.auth import get_user_model
from cities_light.models import Country
from django.db.models import Q, OuterRef, Exists
from datetime import date, timedelta
from matches.models import InterestRequest, Shortlist

User = get_user_model()


class ExploreView(ListView):
    model = User
    template_name = 'explore/index.html'
    context_object_name = 'search_result'
    paginate_by = 6

    def get_queryset(self):
        request = self.request

        interest_subquery = InterestRequest.objects.filter(
            sender=request.user,
            receiver=OuterRef('pk')
        )

        shortlist_subquery = Shortlist.objects.filter(
            user=request.user,
            shortlisted_user=OuterRef('pk')
        )

        queryset = User.objects.exclude(
            id=request.user.id
        ).exclude(matrimony_profile__gender=request.user.matrimony_profile.gender).select_related('matrimony_profile').annotate(
            interest_requested=Exists(interest_subquery),
            shortlisted=Exists(shortlist_subquery),
        )

        # Filters
        query = request.GET.get('q', "")
        religion = request.GET.get('religion', "")
        location = request.GET.get('location', "")
        age_range = request.GET.get('age_range', "")

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

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        request = self.request

        context["query"] = request.GET.get('q', "")
        context["age_range"] = request.GET.get('age_range', "")
        context["location"] = request.GET.get('location', "")
        context["religion"] = request.GET.get('religion', "")
        context["title"] = 'Search'
        context['countries'] = Country.objects.all()

        return context
