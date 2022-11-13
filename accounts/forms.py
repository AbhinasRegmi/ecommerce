from django import forms
from .models import UserBase

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        label='Enter your email.',
        max_length=50,
        required=True,
    )

    username = forms.CharField(
        label='Enter your username.',
        max_length=90,
        required=True,
    )

    password = forms.CharField(
        label='Enter your strong password.',
        required=True,
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Enter password again.',
        required=True,
        widget=forms.PasswordInput
    )

    class Meta:
        model=UserBase
        fields = ['username', 'email', 'password', 'password2']