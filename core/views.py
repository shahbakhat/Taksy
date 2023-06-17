from django.shortcuts import render, redirect
from django .contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from .forms import DriverSignUpForm, PassenegrSignUpForm



from . import forms
# Create your views here.

def home(request):
    return render(request, 'home.html')

def driverHome(request):
    return render(request, 'driver/home.html')


def sign_up(request):
    passenger_signup_form = PassenegrSignUpForm()
    driver_form = DriverSignUpForm()

    if request.method == "POST":
        if 'passenger' in request.POST:
            form = PassenegrSignUpForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email').lower()
                user = form.save(commit=False)
                user.username = email

                print("Passenger form data:", form.cleaned_data)  # Print form data for debugging

                user.save()
                print("Passenger user saved:", user)  # Print user object for debugging

                login(request, user)
                return redirect('/')
        elif 'driver' in request.POST:
            form = DriverSignUpForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email').lower()
                user = form.save(commit=False)
                user.username = email

                print("Driver form data:", form.cleaned_data)  # Print form data for debugging

                user.save()
                print("Driver user saved:", user)  # Print user object for debugging

                login(request, user)
                return redirect('/')

    return render(request, 'sign-up.html', {
        'passenger_signup_form': passenger_signup_form,
        'driver_form': driver_form,
    })

