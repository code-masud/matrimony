from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import User
from profiles.models import MatrimonyProfile, PartnerPreference, ProfilePhoto
from django.forms import inlineformset_factory
from cities_light.models import Country, Region, City


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['on_behalf', 'first_name', 'last_name', 'email', 'phone']


class MatrimonyProfileForm(forms.ModelForm):
    class Meta:
        model = MatrimonyProfile
        fields = [
            'gender', 'date_of_birth', 'height_cm', 'marital_status',
            'religion', 'caste', 'mother_tongue', 'education',
            'occupation', 'annual_income', 'country', 'state', 'city', 'about_me'
        ]

        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "height_cm": forms.Select(attrs={"class": "form-select"}),
            "country": forms.Select(attrs={
                "class": "form-select",
                "hx-get": "/accounts/ajax/load-states/",
                "hx-target": "#id_state",
                "hx-swap": "beforeend",
            }),
            "state": forms.Select(attrs={
                "class": "form-select",
                "hx-get": "/accounts/ajax/load-cities/",
                "hx-target": "#id_city",
                "hx-swap": "beforeend",
            }),
            "city": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initial empty querysets for State and City if Country isn't selected yet
        self.fields['state'].queryset = Region.objects.none()
        self.fields['city'].queryset = City.objects.none()

        # If editing an existing profile, populate the querysets correctly
        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = Region.objects.filter(
                    country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.country:
            self.fields['state'].queryset = self.instance.country.region_set.order_by(
                'name')

        if 'state' in self.data:
            try:
                region_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(
                    region_id=region_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.state:
            self.fields['city'].queryset = self.instance.state.city_set.order_by(
                'name')


class PartnerPreferenceForm(forms.ModelForm):
    class Meta:
        model = PartnerPreference
        fields = [
            'min_age',
            'max_age',
            'min_height_cm',
            'max_height_cm',
            'religion',
            'marital_status',
            'education',
            'occupation',
            'country',
            'state',
            'city',
        ]

        widgets = {
            "min_age": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "max_age": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "min_height_cm": forms.Select(attrs={"class": "form-select"}),
            "max_height_cm": forms.Select(attrs={"class": "form-select"}),
            "country": forms.Select(attrs={
                "class": "form-select",
                "hx-get": "/accounts/ajax/load-states/",
                "hx-target": "#id_state_partner",
                "hx-swap": "beforeend",
            }),
            "state": forms.Select(attrs={
                "class": "form-select",
                "id": "id_state_partner",
                "hx-get": "/accounts/ajax/load-cities/",
                "hx-target": "#id_city_partner",
                "hx-swap": "beforeend",
            }),
            "city": forms.Select(attrs={"class": "form-select", "id": "id_city_partner"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initial empty querysets for State and City if Country isn't selected yet
        self.fields['state'].queryset = Region.objects.none()
        self.fields['city'].queryset = City.objects.none()

        # If editing an existing profile, populate the querysets correctly
        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = Region.objects.filter(
                    country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.country:
            self.fields['state'].queryset = self.instance.country.region_set.order_by(
                'name')

        if 'state' in self.data:
            try:
                region_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(
                    region_id=region_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.state:
            self.fields['city'].queryset = self.instance.state.city_set.order_by(
                'name')


class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = MatrimonyProfile
        fields = ['profile_picture']


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = ProfilePhoto
        fields = ['image', 'is_primary']
