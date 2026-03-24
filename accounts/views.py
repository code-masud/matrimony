from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import User
from profiles.models import MatrimonyProfile, PartnerPreference, ProfilePhoto
from .forms import CustomUserChangeForm, MatrimonyProfileForm, PartnerPreferenceForm, ProfilePhotoForm, GalleryImageForm
from cities_light.models import Region, City
# Create your views here.


class MyProfile(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/index.html'
    # permission_required = ['accounts.view_user']

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
            response = render(self.request, self.row_template, {
                              self.context_object_name: self.object})
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


class UpdateProfileImage(HtmxFormMixin, UpdateView):
    model = MatrimonyProfile
    template_name = 'accounts/partials/profile_image_form.html'
    form_class = ProfilePhotoForm
    row_template = 'accounts/partials/profile_image_row.html'
    context_object_name = 'profile'
    success_url = reverse_lazy('accounts:my_profile')
    permission_required = ['accounts:add_user']
    htmx_trigger = 'closeModal'


class CreateMatrimonyProfile(CreateView):
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
            response = render(self.request, self.row_template, {
                              self.context_object_name: self.object})
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


class CreatePartnerPreference(CreateView):
    model = PartnerPreference
    template_name = 'accounts/partials/preference_form.html'
    form_class = PartnerPreferenceForm
    row_template = 'accounts/partials/preference_row.html'
    context_object_name = 'preference'
    success_url = reverse_lazy('accounts:my_profile')
    permission_required = ['accounts:add_user']
    htmx_trigger = 'closeModal'

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()

        if self.request.headers.get("HX-Request"):
            response = render(self.request, self.row_template, {
                              self.context_object_name: self.object})
            response['HX-Trigger'] = self.htmx_trigger
            return response

        return super().form_valid(form)


class UpdatePartnerPreference(HtmxFormMixin, UpdateView):
    model = PartnerPreference
    template_name = 'accounts/partials/preference_form.html'
    form_class = PartnerPreferenceForm
    row_template = 'accounts/partials/preference_row.html'
    context_object_name = 'preference'
    success_url = reverse_lazy('accounts:my_profile')
    permission_required = ['accounts:add_user']
    htmx_trigger = 'closeModal'


class GalleryCreate(CreateView):
    model = ProfilePhoto
    template_name = 'accounts/partials/gallery_form.html'
    form_class = GalleryImageForm
    row_template = 'accounts/partials/gallery_row.html'
    context_object_name = 'photo'
    success_url = reverse_lazy('accounts:my_profile')
    permission_required = ['accounts:add_user']
    htmx_trigger = 'closeModal'

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()

        if self.request.headers.get("HX-Request"):
            response = render(self.request, self.row_template, {
                              self.context_object_name: self.object})
            response['HX-Trigger'] = self.htmx_trigger
            return response

        return super().form_valid(form)


class GalleryUpdate(HtmxFormMixin, UpdateView):
    model = ProfilePhoto
    template_name = 'accounts/partials/gallery_form.html'
    form_class = GalleryImageForm
    row_template = 'accounts/partials/gallery_row.html'
    context_object_name = 'photo'
    success_url = reverse_lazy('accounts:my_profile')
    permission_required = ['accounts:add_user']
    htmx_trigger = 'closeModal'


def load_states(request):
    country_id = request.GET.get('country')
    states = Region.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'accounts/partials/dropdown_list_options.html', {'items': states})


def load_cities(request):
    state_id = request.GET.get('state')
    cities = City.objects.filter(region_id=state_id).order_by('name')
    return render(request, 'accounts/partials/dropdown_list_options.html', {'items': cities})
