from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from core.passenger import forms
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
import stripe
from core.models import Taxi, Passenger, MyTrips
from django.utils import timezone
import googlemaps
from googlemaps import convert
from googlemaps import distance_matrix
from django.utils.text import slugify
from .forms import TaxiBookingForm
from datetime import datetime
from django.utils.timezone import now
from .forms import BasicUserForm, BasicCustomerForm
from django.http import HttpResponseRedirect,HttpRequest
from core.models import TaxiPassenger,TaxiDriver,User
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from core.models import Passenger
from django.core.exceptions import ObjectDoesNotExist



User = get_user_model()

def home(request):
    return render(request, "welcome.html")



@login_required(login_url="/login/?next=/passenger/")
def profile_page(request):
    user_form = BasicUserForm(instance=request.user)
    passenger_form = BasicCustomerForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)

    if request.method == "POST":
        if request.POST.get('action') == 'update_profile':
            user_form = BasicUserForm(request.POST, instance=request.user)
            passenger_form = BasicCustomerForm(request.POST, request.FILES, instance=request.user)
            if user_form.is_valid() and passenger_form.is_valid():
                user_form.save()
                passenger_form.save()

                messages.success(request, 'Profile updated successfully.')
                return redirect(reverse('passenger:profile'))

        elif request.POST.get('action') == 'update_password':
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)

                messages.success(request, 'Password updated successfully.')
                return redirect(reverse('passenger:profile'))

    return render(request, 'passenger/profile.html', {
        "user_form": user_form,
        "passenger_form": passenger_form,
        "password_form": password_form,
    })



# BOOKING TAXI

@login_required(login_url="/login/?next=/passenger/")

def book_taxi_page(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'passenger'):
        return redirect('login')

    if request.method == "POST":
        pickup_form = TaxiBookingForm(request.POST)
        if pickup_form.is_valid():
            passenger = request.user.passenger

            # Validate pickup address
            gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
            pickup_address = pickup_form.cleaned_data['pickup_address']
            pickup_geocode_result = gmaps.geocode(pickup_address)
            if not pickup_geocode_result:
                messages.error(request, "Invalid pickup address. Please enter a valid address.")
                return redirect(reverse('passenger:book-a-taxi'))
            pickup_location = pickup_geocode_result[0]['geometry']['location']
            pickup_lat = pickup_location['lat']
            pickup_lng = pickup_location['lng']

            # Validate dropoff address
            dropoff_address = pickup_form.cleaned_data['dropoff_address']
            dropoff_geocode_result = gmaps.geocode(dropoff_address)
            if not dropoff_geocode_result:
                messages.error(request, "Invalid dropoff address. Please enter a valid address.")
                return redirect(reverse('passenger:book-a-taxi'))
            dropoff_location = dropoff_geocode_result[0]['geometry']['location']
            dropoff_lat = dropoff_location['lat']
            dropoff_lng = dropoff_location['lng']

            # Calculate the distance using Google Maps Distance Matrix API
            origins = f"{pickup_lat},{pickup_lng}"
            destinations = f"{dropoff_lat},{dropoff_lng}"
            result = gmaps.distance_matrix(origins, destinations, mode='driving')

            # Extract the distance value from the API response
            distance = result['rows'][0]['elements'][0]['distance']['value']
            # Convert distance to kilometers (optional)
            distance_km = distance / 1000

            # Create a new booking instance
            taxi_booking = Taxi(
                taxi_passenger=passenger,
                pickup_address=pickup_address,
                pickup_lat=pickup_lat,
                pickup_lng=pickup_lng,
                dropoff_address=dropoff_address,
                dropoff_lat=dropoff_lat,
                dropoff_lng=dropoff_lng,
                trip_distance=distance_km,
                pickup_datetime=datetime.now(),
                taxi_booking_status=Taxi.TRIP_BOOKED
            )
            taxi_booking.save()

            # Create MyTrips instance
            my_trip = MyTrips(
                booked_passenger=passenger,
                booked_taxi=taxi_booking,
            )
            my_trip.save()

            # Add success message
            messages.success(request, "Booking created successfully!")

            return redirect(reverse('passenger:my-trips'))
        else:
            # Add error messages for form fields with invalid data
            for field, errors in pickup_form.errors.items():
                for error in errors:
                    messages.error(request, f"Invalid {field}: {error}")
    else:
        pickup_form = TaxiBookingForm()

    return render(request, 'passenger/book-a-taxi.html', {
        "pickup_form": pickup_form,
    })
# CANCEL THE TRIP LOGIC

def cancel_trip(request, trip_id):
    try:
        trip = Taxi.objects.get(id=trip_id)
        trip.taxi_booking_status = Taxi.TRIP_CANCELLED  # Update the booking status to 'Trip Cancelled'
        trip.save()

        my_trip = MyTrips.objects.get(booked_taxi=trip)
        my_trip.save()

        messages.success(request, "Trip cancelled successfully!")
    except Taxi.DoesNotExist:
        messages.error(request, "Trip not found.")

    return redirect('passenger:my-trips')

#  PASSENGER TRIPS
@login_required(login_url="/login/?next=/passenger/")

def my_trips_page(request):
    try:
        passenger = request.user.passenger
        booked_trips = Taxi.objects.filter(taxi_passenger=passenger, taxi_booking_status=Taxi.TRIP_BOOKED).order_by('pickup_datetime')
        canceled_trips = Taxi.objects.filter(taxi_passenger=passenger, taxi_booking_status=Taxi.TRIP_CANCELLED).order_by('cancellation_time')

        trips = list(booked_trips) + list(canceled_trips)

        context = {
            'trips': trips,
        }

        return render(request, 'passenger/my-trips.html', context)

    except ObjectDoesNotExist:
        # Handle the case when the user does not have a related passenger object
        # You can adjust this part to fit your desired behavior or redirect the user to an appropriate page
        return render(request, 'passenger/my-trips.html', {'no_passenger': True})



#Payment Method

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required(login_url="/login/?next=/passenger/")

def payment_method_page(request):
    try:
        passenger = request.user.passenger
    except AttributeError:
        return redirect('login')

    if request.method == 'POST':
        stripe.PaymentMethod.detach(passenger.stripe_payment_method_id)
        passenger.stripe_payment_method_id = ''
        passenger.stripe_card_last4 = ''
        passenger.save()
        return redirect('passenger:payment-method')

    if not passenger.stripe_customer_id:
        customer = stripe.Customer.create()
        passenger.stripe_customer_id = customer['id']
        passenger.save()

    stripe_payment_methods = stripe.PaymentMethod.list(
        customer=passenger.stripe_customer_id,
        type='card',
    )

    if stripe_payment_methods and len(stripe_payment_methods.data) > 0:
        payment_method = stripe_payment_methods.data[0]
        passenger.stripe_payment_method_id = payment_method.id
        passenger.stripe_card_last4 = payment_method.card.last4
        passenger.save()
    else:
        passenger.stripe_payment_method_id = ''
        passenger.stripe_card_last4 = ''
        passenger.save()

    client_secret = stripe.SetupIntent.create(
        customer=passenger.stripe_customer_id,
        payment_method_types=['card'],
    ).client_secret

    return render(request, 'passenger/payment-method.html', {
        'passenger': passenger,
        'client_secret': client_secret,
        'STRIPE_API_PUBLIC_KEY': settings.STRIPE_API_PUBLIC_KEY,
    })
