from django.shortcuts import render, redirect
from django .contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from .forms import PassengerSignUpForm
from django.contrib import messages



from . import forms
# Create your views here.

def home(request):
    return render(request, 'home.html')

def driverHome(request):
    return render(request, 'driver/home.html')


import logging

logger = logging.getLogger(__name__)

def sign_up(request):
    logger.debug("Sign up view accessed")  # Log a debug message

    passenger_signup_form = PassengerSignUpForm()

    if request.method == 'POST':
        form = PassengerSignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email').lower()
            user = form.save(commit=False)
            user.username = email

            logger.debug("Passenger form data: %s", form.cleaned_data)  # Log form data

            user.save()
            logger.debug("Passenger user saved: %s", user)  # Log user object

            login(request, user)

            messages.success(request, "You have successfully signed up as a passenger.")

            return redirect('passenger:passenger-profile')

    return render(request, 'sign-up.html', {
        'passenger_signup_form': passenger_signup_form,
    })
