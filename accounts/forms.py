from django import forms
from django.core.exceptions import ValidationError

from .models import UserBase


class RegistrationForm(forms.Form):

    username = forms.CharField(
        label='Username',
        max_length=90,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a username.'
            }),
    )

    email = forms.EmailField(
        label='Email',
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address.'
            }),
    )

    password = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a strong password.'
            }),
    )

    password2 = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password again.'
            }),
    )

    class Meta:
        model=UserBase
        fields = ['username', 'email', 'password', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']

        if UserBase.objects.filter(email=email).count():
            raise ValidationError('email already in use.')

        self.email = email


    def clean_username(self):
        username = self.cleaned_data['username']

        if UserBase.objects.filter(username=username):
            raise ValidationError('try a different username.')

        if len(username) < 4:
            raise ValidationError('username must be at least 4 characters.')

        self.username = username
        

    #since two password are related field they can be processed in clean together

    def clean(self):
        data = super().clean()

        password = data.get('password')
        password2 = data.get('password2')

        if not password == password2:
            self.add_error(field='password', error='two passwords must match.')

        if len(password) < 8:
            self.add_error(field='password', error='length of password must be between 8 - 16 characters')

        if not any(char.isdigit() for char in password):
            self.add_error(field='password', error='there must be at least 1 digit in password')
        
        if not any(char in ['$', '@', '#', '%', '_', '-', '+'] for char in password):
            self.add_error(field='password', error='there should be at least 1 special symbol($, @, #, %, -, _, +).')

        self.password = password

        return data

    def save(self):
        print('save method called.')
        UserBase.objects.create_user(
            email=self.email,
            username=self.username,
            password=self.password
        )