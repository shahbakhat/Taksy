from django.shortcuts import render, redirect
# from .forms import DriverSignUpForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# from core.models import Driver
from django.conf import settings
import requests
from core.models import *


@login_required(login_url="/login/?next=/driver/")
def home(request):
    return redirect(reverse ('driver:available-trps'))

@login_required(login_url="/login/?next=/driver/")
def available_trips_page(request):
    return render(request, 'driver/available-trips.html',{
        "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY
    })


@login_required(login_url="/drive/login")
def my_jobs_page(request):
    available_trips = Taxi.objects.filter(taxi_booking_status=Taxi.TRIP_BOOKED).values()
    return render(request, 'driver/my-jobs.html', {'available_trips': available_trips})


