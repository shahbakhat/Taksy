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
def book_taxi_page(request):  # sourcery skip: assign-if-exp, merge-nested-ifs, swap-if-expression, swap-nested-ifs
    current_customer = request.user.passenger

    if not request.user.passenger.stripe_payment_method_id:

        return redirect(reverse('passenger:payment-method'))

    creating_booking = Taxi.objects.filter(taxi_passenger=current_customer, taxi_booking_status=Taxi.BOOKING_IN_PROGRESS).last()
    # model_instance = creating_booking.first()
    pickup_form = forms.TaxiBookingForm(request.POST, instance=creating_booking)
    if request.method == "POST":
        pickup_form = forms.TaxiBookingForm(request.POST, instance= creating_booking)
        if pickup_form.is_valid():
            creating_booking = pickup_form.save(commit=False)
            creating_booking.taxi_passenger = current_customer
            creating_booking.save()
            return redirect(reverse('passenger:book-a-taxi'))
    # Determine the current step
    # if not creating_booking:
    #     current_step = 1

    return render (request,'passenger/book-a-taxi.html',{
        "taxi": creating_booking,
        "pickup_form": pickup_form,
        # "step":current_step,
    })



#  PASSENGER TRIPS
@login_required(login_url="/login/?next=/passenger/")
def my_trips_page(request):
    return render(request, 'passenger/my-trips.html',)


#Payment Method
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required(login_url="/login/?next=/passenger/")
def payment_method_page(request):  # sourcery skip: hoist-similar-statement-from-if, hoist-statement-from-if
    current_customer = request.user.passenger

    #remover existing Card
    if request.method == "POST":
        stripe.PaymentMethod.detach(current_customer.stripe_payment_method_id)
        current_customer.stripe_payment_method_id = ""
        current_customer.stripe_card_last4 = ""
        current_customer.save()
        return redirect(reverse('passenger:payment-method'))

    # stripe customer info
    if not current_customer.stripe_customer_id:
        customer = stripe.Customer.create()
        current_customer.stripe_customer_id = customer['id']
        current_customer.save()
    #Get the strpe payment method
    stripe_payment_methods  = stripe.PaymentMethod.list(
        customer = current_customer.stripe_customer_id,
        type = "card",
    )
    print (stripe_payment_methods)

    if stripe_payment_methods and len(stripe_payment_methods.data) > 0:
        payment_method = stripe_payment_methods.data[0]
        current_customer.stripe_payment_method_id = payment_method.id
        current_customer.stripe_card_last4 = payment_method.card.last4
        current_customer.save()
    else:
        current_customer.stripe_payment_method_id = ""
        current_customer.stripe_card_last4 = ""
        current_customer.save()
    if not current_customer.stripe_payment_method_id:

        intent = stripe.SetupIntent.create(
            customer= current_customer.stripe_customer_id,
            payment_method_types = ["card"],
                                            )
        return render(request, 'passenger/payment-method.html',
                    {
                        "client_secret": intent.client_secret,
                        "STRIPE_API_PUBLIC_KEY": settings.STRIPE_API_PUBLIC_KEY,
                    },)
    else:
        return render(request, 'passenger/payment-method.html')