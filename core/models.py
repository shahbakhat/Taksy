from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from django.db.models import Sum
from django.shortcuts import reverse
import uuid
from django.utils import timezone


# Create your models here.
def passenger_image_upload(instance, filename):
    return f'passenger/static/photos/{instance.user.username}/{filename}'
class Passenger(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to=passenger_image_upload, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True)
    stripe_customer_id = models.CharField(max_length=225, blank=True)
    stripe_payment_method_id= models.CharField(max_length=225, blank=True)
    stripe_card_last4 = models.CharField(max_length=225, blank=True)
    def __str__(self):
        return self.user.get_full_name() or str(self.user)

# Taxi Driver model
def driver_image_upload(instance, filename):
    return f'driver/static/photos/{instance.user.username}/{filename}'

class Driver(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='driver')
    profile_photo = models.ImageField(upload_to=driver_image_upload, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, default='')
    nta_badge_number = models.CharField(max_length=6, default='N1234')
    vehicle_reg = models.CharField(max_length=100, default='')
    date_of_birth = models.DateTimeField(default=timezone.now)
    spsv_license_expirations = models.DateTimeField(default=timezone.now)
    roof_sign_number = models.CharField(max_length=10, blank=False, default='')
    roof_sign_license_expiry = models.DateTimeField(blank=False, default=timezone.now)
    vehicle_license_disc = models.ImageField(upload_to=driver_image_upload, blank=False, default='')
    spsv_license = models.ImageField(upload_to=driver_image_upload, default='', blank=False, null=False)
    driving_license_number = models.CharField(max_length=200, default='')
    driving_license = models.ImageField(upload_to=driver_image_upload, default='', blank=False, null=False)
    accepted_trips = models.ManyToManyField('MyTrips', related_name='accepted_drivers', blank=True)
    cancelled_trips = models.ManyToManyField('MyTrips', related_name='cancelled_drivers', blank=True)
    current_trips = models.ManyToManyField('MyTrips', related_name='current_drivers', blank=True)
    completed_trips = models.ManyToManyField('MyTrips', related_name='completed_drivers', blank=True)
    trips_distance_covered = models.CharField(max_length=255, default='')
    is_verified = models.BooleanField(default=False)
  # Verification status
    is_verified = models.BooleanField(default=False)

    # Trip statuses
    TRIP_ACCEPTED = 'accepted'
    TRIP_CANCELLED = 'cancelled'
    HAVE_PASSENGER_ONBOARD = 'onboard'
    NO_TRIPS = 'no trips'
    DRIVER_TRIP_STATUS = (
        (TRIP_ACCEPTED, 'Trip has been accepted'),
        (TRIP_CANCELLED, 'Trip has been cancelled'),
        (HAVE_PASSENGER_ONBOARD, 'Passenger Onboard'),
        (NO_TRIPS, 'No trips')
    )

    # Vehicle types
    IS_ELECTRIC = 'electric'
    IS_HYBRID = 'hybrid'
    IS_PETROL = 'petrol'
    DIESEL = 'diesel'
    VEHICLE_TYPES = (
        (IS_ELECTRIC, 'Electric'),
        (IS_HYBRID, 'Hybrid'),
        (IS_PETROL, 'Petrol'),
        (DIESEL, 'Diesel'),
    )

    vehicle_make_and_model = models.CharField(max_length=255, default='')
    vehicle_type = models.CharField(max_length=255, choices=VEHICLE_TYPES, default=IS_ELECTRIC)
    driver_trip_status = models.CharField(max_length=255, choices=DRIVER_TRIP_STATUS, default=NO_TRIPS)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.nta_badge_number} - {self.current_trips}"


# Taxi models
class Taxi (models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable= False)
    slug = models.SlugField(max_length=255, unique=True)
    taxi_passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, null=False)
    taxi_passenger_phone_number =models.CharField(max_length=50,default='')
    taxi_passneger_payment_method = models.CharField(max_length=50,default='')
# Taxi size and status field
    FIVE_SEATER = "5 Seater"
    SEVEN_SEATER = "7 Seater"
    EIGHT_SEATER = "7 Seater"
    TAXI_SIZE = (
        (FIVE_SEATER ,'5 Seater'),
        (SEVEN_SEATER ,' 7 Seater'),
        (EIGHT_SEATER ,' 8 Seater'),
    )
    BOOKING_IN_PROGRESS = 'booking in proccess'
    TRIP_BOOKED = 'booked'
    TAXI_ARRIVED = 'arrived'
    PASSENGER_ONBOAD = 'onboard'
    TRIP_COMPLETED = 'complete'
    TRIP_CANCELLED = 'cancelled'
    STATUSES = (
        (BOOKING_IN_PROGRESS,'Booking in progress'),
        (TAXI_ARRIVED,'Arrived'),
        (TRIP_BOOKED , 'Booked'),
        (PASSENGER_ONBOAD , 'Onboard'),
        (TRIP_CANCELLED , 'Cancelled'),
        (TRIP_COMPLETED , 'Completed')

    )
#Taxi booking details fields
    taxi_size =models.CharField(max_length=10,choices=TAXI_SIZE, default=FIVE_SEATER)
    pickup_address = models.CharField(max_length=255, blank=False, default=None)
    dropoff_address = models.CharField(max_length=255, blank=False, default=None)
    pickup_lng = models.FloatField(default=0.0, null = True)
    pickup_lat = models.FloatField(default=0.0, null = True)
    dropoff_lng = models.FloatField(default=0.0, null = True)
    dropoff_lat = models.FloatField(default=0.0, null = True)
    trip_price = models.FloatField(default=0, null = True)
    taxi_booking_status = models.CharField(max_length=100, choices=STATUSES)
    trip_distance = models.DecimalField(default=0, null=True)
    description = models.CharField(max_length=500, default='')
    trip_fare = models.FloatField(default=0)
    duration = models.IntegerField(default=0)
    pickup_datetime = models.DateTimeField(default=timezone.now)
    trip_distance = models.CharField(max_length=255, default=None)
    booking_time = models.DateTimeField(default=timezone.now)
    cancellation_time = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.taxi_passenger.user.get_full_name()}'s Booking is - {self.taxi_booking_status} - From '{self.pickup_address}' |--> '{self.dropoff_address}' @ Date and time :[{self.pickup_datetime}]'"

class MyTrips(models.Model):
    booked_passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    booked_taxi = models.ForeignKey(Taxi, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.booked_passenger.user.get_full_name()}'s Booking - {self.booked_taxi}"
