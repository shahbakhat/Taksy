from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from core.passenger import forms
from django.contrib import messages
@login_required(login_url="/login/?next=/passenger/")
def home(request):
    return redirect(reverse('passenger:profile'))

@login_required(login_url="/login/?next=/passenger/")
def profile_page(request):
    user_form = forms.BasicUserForm
    passenger_form = forms.BasicCustomerForm(instance=request.user.passenger)

    if request.method == "POST":
         user_from = forms.BasicCustomerForm(request.POST, instance=request.user)
         passenger_form = forms.BasicCustomerForm(request.POST, request.FILES, instance=request.user.passenger)
         if user_from.is_valid() and passenger_form.is_valid():
             user_from.save()
             passenger_form.save()

             #Profile update toast
             messages.success(request,'Your profile has been updated')
             return redirect(reverse('passenger:profile'))

    return render(request, 'passenger/profile.html',
                  {"user_form": user_form,
                   "passenger_form": passenger_form,
                   }
                  )

