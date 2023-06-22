from django import forms
from django.core.exceptions import ValidationError
from .models import User

class PassengerSignUpForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'required': True}),
    )
    email = forms.EmailField(
        max_length=250,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address', 'required': True}),
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'required': True}),
    )
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name', 'required': True}),
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name', 'required': True}),
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")
        return email
