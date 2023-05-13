from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=250)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
    # Funcion to return clean data in form if dictionary
    # String and primary keys will be returned asobjects
    def clean_field(self):
        data = self.cleaned_data('email').lowercase()
        if User.objects.filter(email=data).exists:
            raise ValidationError("The email address already exists")
        return data.cleaned_data('email')



