from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

User = get_user_model()


class ExploreView(TemplateView):
    template_name = 'explore/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Search'

        search_result = User.objects.exclude(id=self.request.user.id).all()
        context['search_result'] = search_result
        return context
