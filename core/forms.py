from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class PassengerSignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=250,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        label=''
    )
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        label=''
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        label=''
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("The email address already exists")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        validate_password(password1)
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match')
        
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def is_valid(self):
        valid = super().is_valid()
        if valid:
            for field in self.fields.values():
                field.widget.attrs['class'] += ' is-valid'
        else:
            for field in self.errors.keys():
                self.fields[field].widget.attrs['class'] += ' is-invalid'
        return valid





# class DriverSignUpForm(UserCreationForm):
#     phone_number = forms.CharField(max_length=50)
#     email = forms.EmailField(max_length=250)
#     first_name = forms.CharField(max_length=150)
#     last_name = forms.CharField(max_length=150)
#     password1 = forms.PasswordInput(attrs={'autofocus': False})
#     password2 = forms.PasswordInput(attrs={'autofocus': False})

#     class Meta:
#         model = User
#         fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
#     def clean_email(self):
#         email = self.cleaned_data['email'].lower()
#         if User.objects.filter(email=email):
#             raise ValidationError("The email address already exists")
#         return email
