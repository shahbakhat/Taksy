from django.shortcuts import render

# Create your views here.
def home(request):
    return render (request, 'home.html')

def passenger_page(request):
    return render (request, 'passenger.html')

def driver_page(request):
    return render (request, 'driver.html')
def login(request):
    return render (request, 'login.html')
def login(request):
    return render (request, 'logout.html')
