from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render (request, 'home.html')

@login_required()
def passenger_page(request):
    return render (request, 'passenger.html')
@login_required()
def driver_page(request):
    return render (request, 'driver.html')
