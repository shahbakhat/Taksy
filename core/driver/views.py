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
    return render(request,'driver/driver-home.html')

@login_required(login_url="/login/?next=/driver/")
def driver_trip_view(request):
    trips_to_views =Taxi.objects.filter(taxi_booking_status=Taxi.TRIP_BOOKED).values()
    return render(request, 'driver/trips-view.html', {'trips_to_views': trips_to_views},)

@login_required(login_url="/login/?next=/driver/")
def driver_home_page(request):
    trips_to_views =Taxi.objects.filter(taxi_booking_status=Taxi.TRIP_BOOKED).values()
    return render(request, 'driver/driver-home.html', {'trips_to_views': trips_to_views},
                  {
        "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY,
    })





