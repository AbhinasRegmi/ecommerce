from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
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

        #here email, other fields are not returned because i have written custom
        #save method and accessing email from self.email

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
    
        user = UserBase.objects.create_user(
            email=self.email,
            username=self.username,
            password=self.password
        )

        return user


class LoginForm(forms.Form):

    email = forms.EmailField(
        label='Email',
        required=True,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email.'
            }
        )
    )

    password = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password.'
            }
        )
    )

    def clean(self):
        data = super().clean()

        email = data.get('email')
        password = data.get('password')


        self.user = authenticate(email=email, password=password, is_active=True)
        
        if not self.user:
            self.add_error(
                field='email', 
                error="Enter correct credentials. Are you sure you're verified?"
            )

        return data

    def get_user(self):
        return self.user



class ProfileUpdateForm(forms.ModelForm):

    firstname = forms.CharField(
        label='Firstname*',
        required=True,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your firstname.'
            }
        )
    )

    lastname = forms.CharField(
        label='Lastname*',
        required=True,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your lastname.'
            }
        )
    )

    about = forms.CharField(
        label='Bio',
        required=False,
        max_length=500,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Write something about yourself.'
            }
        )
    )
    
    country = forms.Select(
        attrs={
            'class': 'form-control'
        }
    )

    phone = forms.CharField(
        label='Phonenumber*',
        required=True,
        max_length=10,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number.'
            }
        )
    )
    
    class Meta:
        model = UserBase
        fields = ['firstname', 'lastname', 'profile', 'about', 'country', 'phone']

    def clean_firstname(self):
        firstname = self.cleaned_data['firstname']
        if not len(firstname) > 3:
            raise ValidationError('Firstname must be at least  3 alphabets.')

        return firstname

    
    def clean_lastname(self):
        lastname = self.cleaned_data['lastname']
        if not len(lastname) > 3:
            raise ValidationError('Lastname must be at least 3 alphabets.')

        return lastname

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if not len(phone) == 10:
            raise ValidationError('Phone number be of 10 digits only.')

        return phone


class ResetYourPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(
            attrs={
                'autocomplete': 'email',
                'class': 'form-control',
                'placeholder': 'Enter your email here.'
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data['email']

        if not UserBase.objects.filter(email=email, is_active=True).exists():
            raise ValidationError('Please enter a valid email.')

        return email

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name):

        # for now the reset link will be printed to terminal later it will be sent with celery
        email = context.get('email')
        domain = context.get('domain')
        uid = context.get('uid')
        token = context.get('token')

        url = f"http://{domain}/accounts/reset/confirm/{uid}/{token}/"

        print('\n\n\n')
        print(url)
        print('\n\n\n')



class PasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                'class': 'form-control',
                'placeholder': 'Enter your new password.'
        }),
    )

    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                'class': 'form-control',
                'placeholder': 'Enter new password again.'
        }),
    )