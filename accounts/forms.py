from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import User
from profiles.models import MatrimonyProfile

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