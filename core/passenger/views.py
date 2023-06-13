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
import googlemaps
from googlemaps import convert
from googlemaps import distance_matrix
from django.utils.text import slugify






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
    current_customer = request.user.passenger

    if not request.user.passenger.stripe_payment_method_id:
        return redirect(reverse('passenger:payment-method'))

    creating_booking = Taxi.objects.filter(taxi_passenger=current_customer, taxi_booking_status=Taxi.BOOKING_IN_PROGRESS).last()
    phone_number = current_customer.phone_number
    taxi_passenger_payment_method = current_customer.stripe_card_last4
    description = Taxi.description

    if request.method == "POST":
        pickup_form = forms.TaxiBookingForm(request.POST, instance=creating_booking)
        if request.POST.get('booking-info') == '1':
            if pickup_form.is_valid():
                # Process the form data and save the booking
                creating_booking = pickup_form.save(commit=False)
                creating_booking.taxi_passenger = current_customer

                # Generate a unique slug for the taxi based on its attributes
                slug = slugify(f"{creating_booking.taxi_passenger}-{creating_booking.pickup_address}-{creating_booking.dropoff_address}")
                creating_booking.slug = slug

                creating_booking.save()

                # Calculate the distance using Google Maps Distance Matrix API
                gmaps = googlemaps.Client(key='AIzaSyANA9ozNn4mr7ljTh97_4jgeeryhi5tsio')
                origins = f"{creating_booking.pickup_lat},{creating_booking.pickup_lng}"
                destinations = f"{creating_booking.dropoff_lat},{creating_booking.dropoff_lng}"
                result = gmaps.distance_matrix(origins, destinations, mode='driving')

                # Extract the distance value from the API response
                distance = result['rows'][0]['elements'][0]['distance']['value']
                # Convert distance to kilometers (optional)
                distance_km = distance / 1000

                # Save the distance to the booking model
                creating_booking.distance = distance_km
                creating_booking.save()

                # Clear the form
                pickup_form = forms.TaxiBookingForm()

                return redirect(reverse('passenger:book-a-taxi') + '?show_trip_details=true')
            else:
                pickup_form = forms.TaxiBookingForm(instance=creating_booking)
        elif request.POST.get('confirm-booking') == '2':
            return redirect(reverse('passenger:book-a-taxi') + '?show_trip_details=true')

    else:
        pickup_form = forms.TaxiBookingForm(instance=creating_booking)

    show_trip_details = request.GET.get('show_trip_details') == 'true'

    return render(request, 'passenger/book-a-taxi.html', {
        "taxi": creating_booking,
        "pickup_form": pickup_form,
        "phone_number": phone_number,
        "show_trip_details": show_trip_details,
        "taxi_passenger_payment_method": taxi_passenger_payment_method,
        "description": description,
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