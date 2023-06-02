from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from core.passenger import forms
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
import stripe
from core.models import Taxi, Passenger
from django.utils import timezone
from django.http import JsonResponse





@login_required(login_url="/login/?next=/passenger/")
def home(request):
    return redirect(reverse('passenger:profile'))

#  PROFILE PAGE
@login_required(login_url="/login/?next=/passenger/")
def profile_page(request):
    user_form = forms.BasicUserForm(instance=request.user)
    passenger_form = forms.BasicCustomerForm(instance=request.user.passenger)
    password_form = PasswordChangeForm(request.user)

    if request.method == "POST":
        if request.POST.get('action') == 'update_profile':

            user_form = forms.BasicUserForm(
                request.POST, instance=request.user)
            passenger_form = forms.BasicCustomerForm(
                request.POST, request.FILES, instance=request.user.passenger)

        if user_form.is_valid() and passenger_form.is_valid():
            user_form.save()
            passenger_form.save()

            # Profile update toast
            messages.success(request, 'profile updated successfully.')
            return redirect(reverse('passenger:profile'))

        elif request.POST.get('action') == 'update_password':
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)


                messages.success(request, 'password updated successfully.')
                return redirect(reverse('passenger:profile'))

    return render(request, 'passenger/profile.html',
                  {"user_form": user_form,
                   "passenger_form": passenger_form,
                   "password_form": password_form,
                   }
                  )


# BOOKING TAXI

@login_required(login_url="/login/?next=/passenger/book-a-taxi")
def book_taxi_page(request):
    current_customer = request.user.customer
    creating_booking = Taxi.objects.filter(taxi_passenger= current_customer, taxi_status = Taxi.BOOKING_IN_PROGRESS)
    booking_step1_form = forms.TripBookingForm(instance=creating_booking)
    booking_step2_form = forms.TripBookingForm(instance=creating_booking)
    # Determine the current step

    return render (request,'passenger/book-a-taxi.html',{
        "taxi": creating_booking,
        "booking_step1_form":booking_step1_form,
        "booking_step2_form":booking_step2_form,
    })



#  PASSENGER TRIPS
@login_required(login_url="/login/?next=/passenger/")
def my_trips_page(request):
    return render(request, 'passenger/my-trips.html',)


#Payment Method
stripe.api_key = settings.STRIPE_SECRET_KEY
@login_required(login_url="/login/?next=/passenger/")
def payment_method_page(request):
    current_customer = request.user.passenger

    # stripe customer info
    if not current_customer.stripe_customer_id:
        customer = stripe.Customer.create()
        current_customer.stripe_customer_id = customer['id']
        current_customer.save()

    intent = stripe.SetupIntent.create(
        customer= current_customer.stripe_customer_id,
                                        )
    return render(request, 'passenger/payment-method.html',
                  {
                      "client_secret": intent.client_secret,
                      "STRIPE_API_PUBLIC_KEY": settings.STRIPE_API_PUBLIC_KEY,
                  })