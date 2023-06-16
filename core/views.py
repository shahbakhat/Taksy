from django.shortcuts import render, redirect
from django .contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from .forms import DriverSignUpForm,PassenegerSignUpForm



from . import forms
# Create your views here.

def home(request):
    return render(request, 'home.html')

def driverHome(request):
    return render(request, 'driver/home.html')

def sign_up(request):
    passenger_form = forms.PassenegerSignUpForm()
    driver_form = forms.DriverSignUpForm()

    if request.method == "POST":
        if 'passenger' in request.POST:
            form = forms.PassenegerSignUpForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email').lower()
                user = form.save(commit=False)
                user.username = email
                user.save()

                login(request, user)
                return redirect('/')
        elif 'driver' in request.POST:
            form = forms.DriverSignUpForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email').lower()
                user = form.save(commit=False)
                user.username = email
                user.save()

                login(request, user)
                return redirect('/')

    return render(request, 'sign-up.html', {
        'passenger_form': passenger_form,
        'driver_form': driver_form,
    })
