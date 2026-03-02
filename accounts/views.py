from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import User
from profiles.models import MatrimonyProfile
from .forms import CustomUserChangeForm, MatrimonyProfileForm


# Create your views here.
class MyProfile(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'accounts/index.html'
    permission_required = ['accounts.view_user']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'My Profile'
        return context

class HtmxFormMixin:
    row_template = None
    htmx_trigger = 'closeModal'

    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get("HX-Request"):
            response = render(self.request, self.row_template, {self.context_object_name: self.object})
            response['HX-Trigger'] = self.htmx_trigger
            return response
        
        return super().form_valid(form)
    
class UpdateUser(HtmxFormMixin, UpdateView):
    model = User
    template_name = 'accounts/partials/user_form.html'
    form_class = CustomUserChangeForm
    row_template = 'accounts/partials/user_row.html'
    context_object_name = 'user'
    success_url = reverse_lazy('accounts:my_profile')
    permission_required = ['accounts:add_user']
    htmx_trigger = 'closeModal'

class CreateMatrimonyProfile(HtmxFormMixin, CreateView):
    model = MatrimonyProfile
    template_name = 'accounts/partials/profile_form.html'
    form_class = MatrimonyProfileForm
    row_template = 'accounts/partials/profile_row.html'
    context_object_name = 'profile'
    success_url = reverse_lazy('accounts:my_profile')
    permission_required = ['accounts:add_user']
    htmx_trigger = 'closeModal'

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()

        if self.request.headers.get("HX-Request"):
            response = render(self.request, self.row_template, {self.context_object_name: self.object})
            response['HX-Trigger'] = self.htmx_trigger
            return response
        
        return super().form_valid(form)

class UpdateMatrimonyProfile(HtmxFormMixin, UpdateView):
    model = MatrimonyProfile
    template_name = 'accounts/partials/profile_form.html'
    form_class = MatrimonyProfileForm
    row_template = 'accounts/partials/profile_row.html'
    context_object_name = 'profile'
    success_url = reverse_lazy('accounts:my_profile')
    permission_required = ['accounts:add_user']
    htmx_trigger = 'closeModal'