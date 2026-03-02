from django import forms
from .models import User
from django.contrib.auth.forms import UserChangeForm

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['on_behalf', 'first_name', 'last_name', 'email', 'phone']
