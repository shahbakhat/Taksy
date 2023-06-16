from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class PassenegerSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=250)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    password1 = forms.PasswordInput(attrs={'autofocus': False})
    password2 = forms.PasswordInput(attrs={'autofocus': False})
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
    # Funcion to return clean data in form if dictionary
    # String and primary keys will be returned asobjects
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email):
            raise ValidationError("The email address already exists")
        return email


class DriverSignUpForm(UserCreationForm):
    phone_number = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=250)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    password1 = forms.PasswordInput(attrs={'autofocus': False})
    password2 = forms.PasswordInput(attrs={'autofocus': False})

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email):
            raise ValidationError("The email address already exists")
        return email
