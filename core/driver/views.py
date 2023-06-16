from django.shortcuts import render, redirect
# from .forms import DriverSignUpForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# from core.models import Driver


@login_required(login_url="/login/?next=/driver/")
def home(request):
    return render(request, '/drivers/home.html')
