from django import forms
from accounts.models import UserBase

class CheckoutBasketForm(forms.ModelForm):

    firstname = forms.CharField(
        required=True, 
        label='FirstName',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your firstname here.',
                'class': 'form-control',
            }
        )
    )

    lastname = forms.CharField(
        required=True,
        label='LastName',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your lastname here.',
                'class': 'form-control',
            }
        )
    )

    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter your email here.',
                'class': 'form-control',
            }
        )
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

    country = forms.Select(
        attrs={
            'class': 'form-control'
        }
    )

    
    class Meta:
        model = UserBase
        fields = ['firstname', 'lastname', 'email', 'phone','country']