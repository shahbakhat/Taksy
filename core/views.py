from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from . import forms
# Create your views here.
def home(request):
    return render (request, 'home.html')

@login_required()
def passenger_page(request):
    return render (request, 'home.html')
@login_required()
def driver_page(request):
    return render (request, 'home.html')

def sign_up(request):
    form = forms.SignUpForm()
    return render (request, 'sign-up.html')
