from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from core.passenger import forms

@login_required()
def home(request):
    return redirect(reverse('passenger:profile'))

@login_required(login_url="/login/?next=/passenger/")
def profile_page(request):
    user_form = forms.BasicUserForm

    return render(request, 'passenger/profile.html',
                  {"user_form": user_form}
                  )

