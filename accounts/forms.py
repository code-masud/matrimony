from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import User
from profiles.models import MatrimonyProfile, PartnerPreference, ProfilePhoto
from django.forms import inlineformset_factory

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['on_behalf', 'first_name', 'last_name', 'email', 'phone']

class MatrimonyProfileForm(forms.ModelForm):
    class Meta:
        model = MatrimonyProfile
        fields = [
            'gender',
            'date_of_birth', 
            'height_cm', 
            'marital_status', 
            'religion', 
            'caste', 
            'mother_tongue', 
            'education', 
            'occupation', 
            'annual_income',
            'country',
            'state',
            'city',
            'about_me'
        ]

        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "height": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
        }

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
            'country',
            'city',
            'education',
            'occupation',
        ]

        widgets = {
            "min_age": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "max_age": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "min_height_cm": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "max_height_cm": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
        }

class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = MatrimonyProfile
        fields = ['profile_picture']

class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = ProfilePhoto
        fields = ['image', 'is_primary']
