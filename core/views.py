from django.urls import reverse_lazy
from .models import User,TaxiPassenger,TaxiDriver,Driver,Passenger
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import User
from django.shortcuts import render
from .forms import PassengerSignUpForm, DriverSignUpForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from . import forms
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model, logout ,authenticate, login
from django.db import transaction
from django.urls import reverse
from django.views.generic import TemplateView


User = get_user_model()

def home(request):
        return render(request, 'welcome.html')



class CustomLogoutView(TemplateView):
    template_name = 'welcome.html'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return render(request, 'welcome.html')


class PassengerLoginView(LoginView):
    template_name = 'registration/passenger-login.html'
    success_url = ('passenger:profile')

class DriverLoginView(LoginView):
    template_name = 'registration/driver-login.html'
    success_url = reverse_lazy('driver:driver-home')



def driverHome(request):
    return render(request, 'driver/driver-home.html')



def sign_up(request):
    passenger_signup_form = forms.PassengerSignUpForm()
    driver_signup_form = forms.DriverSignUpForm()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'passenger_signup':
            form = forms.PassengerSignUpForm(request.POST)
            role = get_user_model().Role.TAXIPASSENGER
        elif form_type == 'driver_signup':
            form = forms.DriverSignUpForm(request.POST)
            role = get_user_model().Role.TAXIDRIVER
        else:
            form = None
            role = None

        if form and form.is_valid():
            with transaction.atomic():
                user = get_user_model().objects.create_user(
                    email=form.cleaned_data['email'],
                    username=form.cleaned_data['email'],  # Use the email as the username
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    role=role
                )

                if role == get_user_model().Role.TAXIPASSENGER:
                    passenger = Passenger(user=user)
                    # Update passenger fields here
                    passenger.save()

                    # Authenticate the user
                    authenticated_user = authenticate(request, username=user.username, password=form.cleaned_data['password'])
                    if authenticated_user:
                        login(request, authenticated_user)
                        messages.success(request, "You have successfully signed up as a passenger.")
                        return redirect('passenger:profile')
                    else:
                        messages.error(request, "Failed to authenticate. Please try logging in.")
                        return redirect('passenger-login')
                elif role == get_user_model().Role.TAXIDRIVER:
                    driver = Driver(user=user)
                    # Update driver fields here
                    driver.save()

                    # Authenticate the user
                    authenticated_user = authenticate(request, username=user.username, password=form.cleaned_data['password'])
                    if authenticated_user:
                        login(request, authenticated_user)
                        messages.success(request, "You have successfully signed up as a driver.")
                        return redirect('driver:driver-home')
                    else:
                        messages.error(request, "Failed to authenticate. Please try logging in.")
                        return redirect('driver-login')
                else:
                    form = None
                    role = None
                    messages.error(request, "Unfortunately, an error occurred. Please try again.")
                    return redirect('sign-up')

    return render(request, 'sign-up.html', {
        'passenger_signup_form': passenger_signup_form,
        'driver_signup_form': driver_signup_form,
    })
