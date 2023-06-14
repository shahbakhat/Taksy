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


def validate_address(address):
    gmaps = googlemaps.Client(key='YOUR_API_KEY')  # Replace with your API key
    geocode_result = gmaps.geocode(address)

    if not geocode_result:
        return False

    location = geocode_result[0]['geometry']['location']
    return location['lat'], location['lng']

@login_required(login_url="/login/?next=/passenger/")
def book_taxi_page(request):
    current_customer = request.user.passenger

    if not request.user.passenger.stripe_payment_method_id:
        return redirect(reverse('passenger:payment-method'))

    phone_number = current_customer.phone_number
    taxi_passenger_payment_method = current_customer.stripe_card_last4

    if request.method == "POST":
        pickup_form = forms.TaxiBookingForm(request.POST)
        if request.POST.get('booking-info') == '1':
            if pickup_form.is_valid():
                # Validate pickup address
                pickup_address = pickup_form.cleaned_data['pickup_address']
                pickup_latlng = validate_address(pickup_address)
                if not pickup_latlng:
                    messages.error(request, "Invalid pickup address. Please enter a valid address.")
                    return redirect(reverse('passenger:book-a-taxi'))

                # Validate dropoff address
                dropoff_address = pickup_form.cleaned_data['dropoff_address']
                dropoff_latlng = validate_address(dropoff_address)
                if not dropoff_latlng:
                    messages.error(request, "Invalid dropoff address. Please enter a valid address.")
                    return redirect(reverse('passenger:book-a-taxi'))

                # Create a new booking instance
                creating_booking = Taxi(taxi_passenger=current_customer)

                # Assign form data to the booking instance
                creating_booking.pickup_address = pickup_address
                creating_booking.pickup_lat = pickup_latlng[0]
                creating_booking.pickup_lng = pickup_latlng[1]
                creating_booking.dropoff_address = dropoff_address
                creating_booking.dropoff_lat = dropoff_latlng[0]
                creating_booking.dropoff_lng = dropoff_latlng[1]
                pickup_date = pickup_form.cleaned_data['pickup_date']
                pickup_time = pickup_form.cleaned_data['pickup_time'].strftime('%H:%M:%S')
                pickup_datetime_str = f"{pickup_date} {pickup_time}"
                pickup_datetime = datetime.fromisoformat(pickup_datetime_str)
                creating_booking.pickup_time = pickup_datetime

                # Generate a unique slug for the taxi based on its attributes
                slug = slugify(f"{creating_booking.taxi_passenger}-{creating_booking.pickup_address}-{creating_booking.dropoff_address}")
                creating_booking.slug = slug

                # Calculate the distance using Google Maps Distance Matrix API
                gmaps = googlemaps.Client(key='YOUR_API_KEY')  # Replace with your API key
                origins = f"{creating_booking.pickup_lat},{creating_booking.pickup_lng}"
                destinations = f"{creating_booking.dropoff_lat},{creating_booking.dropoff_lng}"
                result = gmaps.distance_matrix(origins, destinations, mode='driving')

                # Extract the distance value from the API response
                distance = result['rows'][0]['elements'][0]['distance']['value']
                # Convert distance to kilometers (optional)
                distance_km = distance / 1000

                # Save the distance to the booking model
                creating_booking.distance = distance_km

                # Retrieve the description from the Taxi model instance
                creating_booking.description = pickup_form.cleaned_data['description']
                # Save the current timestamp as the booking time
                creating_booking.pickup_time = datetime.now()

                creating_booking.save()

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
        pickup_form = forms.TaxiBookingForm()  # Create a new form instance on reload

    show_trip_details = request.GET.get('show_trip_details') == 'true'

    return render(request, 'passenger/book-a-taxi.html', {
        "pickup_form": pickup_form,
        "phone_number": phone_number,
        "show_trip_details": show_trip_details,
        "taxi_passenger_payment_method": taxi_passenger_payment_method,
    })


    
#  PASSENGER TRIPS

@login_required(login_url="/login/?next=/passenger/")
def my_trips_page(request):
    current_user_trips = Taxi.objects.filter(taxi_passenger=request.user.passenger).order_by('pickup_time')

    context = {
        'trips': current_user_trips,
    }

    if not current_user_trips:
        context['no_trips'] = True

    return render(request, 'passenger/my-trips.html', context)

@login_required(login_url="/login/?next=/passenger/")
def cancel_trip(request, trip_id):
    try:
        trip = get_object_or_404(Taxi, id=trip_id, taxi_booking_status=Taxi.BOOKING_IN_PROGRESS)
        trip.delete()
        messages.success(request, "Booking deleted successfully!")
        return redirect(reverse('passenger:my-trips'))
    except Taxi.DoesNotExist:
        messages.error(request, "Booking not found or cannot be deleted.")
    
    return redirect(reverse('passenger:my-trips'))












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