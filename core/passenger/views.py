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


@login_required(login_url="/login/?next=/passenger/")
def book_taxi_page(request):
    current_customer = request.user.passenger

    if not request.user.passenger.stripe_payment_method_id:
        return redirect(reverse('passenger:payment-method'))

    phone_number = current_customer.phone_number
    taxi_passenger_payment_method = current_customer.stripe_card_last4

    if request.method == "POST":
        pickup_form = TaxiBookingForm(request.POST)
        if request.POST.get('booking-info') == '1':
            if pickup_form.is_valid():
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
                creating_booking = Taxi(
                taxi_passenger=current_customer,
                taxi_passenger_phone_number=phone_number,
                taxi_passneger_payment_method=taxi_passenger_payment_method,
                pickup_address=pickup_address,
                pickup_lat=pickup_lat,
                pickup_lng=pickup_lng,
                dropoff_address=dropoff_address,
                dropoff_lat=dropoff_lat,
                dropoff_lng=dropoff_lng,
                trip_distance=distance_km,
                description=pickup_form.cleaned_data['description'],
                pickup_datetime=datetime.now(),
                taxi_booking_status=Taxi.TRIP_BOOKED  # Set the booking status to 'Booking in progress'
            )

                # Generate a unique slug for the taxi based on its attributes
                slug = slugify(f"{creating_booking.taxi_passenger}-{creating_booking.pickup_address}-{creating_booking.dropoff_address}")
                creating_booking.slug = slug

                creating_booking.save()

                # Create MyTrips instance
                my_trip = MyTrips(
                    booked_passenger=current_customer,
                    booked_taxi=creating_booking,
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

        elif request.POST.get('confirm-booking') == '2':
            return redirect(reverse('passenger:book-a-taxi') + '?show_trip_details=true')

    else:
        pickup_form = TaxiBookingForm()  # Create a new form instance on reload

    show_trip_details = request.GET.get('show_trip_details') == 'true'

    return render(request, 'passenger/book-a-taxi.html', {
        "pickup_form": pickup_form,
        "phone_number": phone_number,
        "show_trip_details": show_trip_details,
        "taxi_passenger_payment_method": taxi_passenger_payment_method,
    })
# CANCEL THE TRIP LOGIC
@login_required(login_url="/login/?next=/passenger/")

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
@login_required(login_url="/login/?next=/passenger/")
def my_trips_page(request):
    booked_trips = Taxi.objects.filter(taxi_passenger=request.user.passenger, taxi_booking_status=Taxi.TRIP_BOOKED).order_by('pickup_datetime')
    canceled_trips = Taxi.objects.filter(taxi_passenger=request.user.passenger, taxi_booking_status=Taxi.TRIP_CANCELLED).order_by('-cancellation_time')

    trips = list(booked_trips) + list(canceled_trips)

    context = {
        'trips': trips,
    }

    if not trips:
        context['no_trips'] = True

    return render(request, 'passenger/my-trips.html', context)



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