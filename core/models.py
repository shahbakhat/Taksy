from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.utils import timezone
import uuid
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        TAXIPASSENGER = "TAXIPASSENGER", "Taxi Passenger"
        TAXIDRIVER = "TAXIDRIVER", "Taxi Driver"

    base_role = "OTHER"

    role = models.CharField(max_length=50, choices=Role.choices, default=base_role)

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.role == self.base_role:
                if self.__class__ == TaxiPassenger:
                    self.role = self.Role.TAXIPASSENGER
                elif self.__class__ == TaxiDriver:
                    self.role = self.Role.TAXIDRIVER
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_full_name()} - {self.get_role_display()}"



class TaxiPassenger(User):
    base_role = User.Role.TAXIPASSENGER

    def welcome(self):
        if self.role == User.Role.TAXIDRIVER:
            return "Welcome to Taksi!"
        else:
            return "Access denied. Only Taxi Drivers are allowed."


class TaxiDriver(User):
    base_role = User.Role.TAXIDRIVER

    def welcome(self):
        if self.role == User.Role.TAXIDRIVER:
            return "Welcome, Taxi Driver!"
        else:
            return "Access denied. Only Taxi Drivers are allowed."

def passenger_image_upload(instance, filename):
    return f'passenger/static/photos/{instance.user.username}/{filename}'
class Passenger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='passenger')
    profile_photo = models.ImageField(upload_to=passenger_image_upload, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True)
    stripe_customer_id = models.CharField(max_length=225, blank=True)
    stripe_payment_method_id = models.CharField(max_length=225, blank=True)
    stripe_card_last4 = models.CharField(max_length=225, blank=True)

    def __str__(self):
        return self.user.get_full_name() or str(self.user)

def driver_image_upload(instance, filename):
    return f'driver/static/photos/{instance.user.username}/{filename}'
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
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
    accepted_trips = models.ManyToManyField('Taxi', related_name='booked', blank=True)
    cancelled_trips = models.ManyToManyField('Taxi', related_name='cancelled', blank=True)
    current_trips = models.ManyToManyField('Taxi', related_name='onboard', blank=True)
    completed_trips = models.ManyToManyField('Taxi', related_name='completed', blank=True)
    trips_distance_covered = models.ManyToManyField('Taxi',related_name='trips_distance_covered', default='')
    is_verified = models.BooleanField(default=False)

    # Verification status
    is_verified = models.BooleanField(default=False)

    # Trip statuses
    TRIP_ACCEPTED = 'accepted'
    TRIP_CANCELLED = 'cancelled'
    HAVE_PASSENGER_ONBOARD = 'onboard'
    COMPLETED_TRIPS = 'completed'
    NO_TRIPS = 'no trips'
    DRIVER_TRIP_STATUS = (
        (NO_TRIPS , 'No trips'),
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



def create_passenger_profile(sender, instance, created, **kwargs):
    if created and instance.role == User.Role.TAXIPASSENGER:
        Passenger.objects.get_or_create(user=instance)


def create_driver_profile(sender, instance, created, **kwargs):
    if created and instance.role == User.Role.TAXIDRIVER:
        Driver.objects.get_or_create(user=instance)


post_save.connect(create_passenger_profile, sender=TaxiPassenger)
post_save.connect(create_driver_profile, sender=TaxiDriver)


# Taxi model
class Taxi(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=255, unique=True)
    taxi_passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, null=False)
    taxi_passenger_phone_number = models.CharField(max_length=50, default='')

    # Taxi size and status field
    FIVE_SEATER = "5 Seater"
    SEVEN_SEATER = "7 Seater"
    EIGHT_SEATER = "8 Seater"
    TAXI_SIZE = (
        (FIVE_SEATER, '5 Seater'),
        (SEVEN_SEATER, '7 Seater'),
        (EIGHT_SEATER, '8 Seater'),
    )

    BOOKING_IN_PROGRESS = 'booking in progress'
    TRIP_BOOKED = 'booked'
    TAXI_ARRIVED = 'arrived'
    PASSENGER_ONBOARD = 'onboard'
    TRIP_COMPLETED = 'complete'
    TRIP_CANCELLED = 'cancelled'
    STATUSES = (
        (BOOKING_IN_PROGRESS, 'Booking in progress'),
        (TAXI_ARRIVED, 'Arrived'),
        (TRIP_BOOKED, 'Booked'),
        (PASSENGER_ONBOARD, 'Onboard'),
        (TRIP_CANCELLED, 'Cancelled'),
        (TRIP_COMPLETED, 'Completed')
    )

    # Taxi booking details fields
    taxi_size = models.CharField(max_length=10, choices=TAXI_SIZE, default=FIVE_SEATER)
    pickup_address = models.CharField(max_length=255, blank=False, default=None)
    dropoff_address = models.CharField(max_length=255, blank=False, default=None)
    pickup_lng = models.DecimalField(max_digits=9, decimal_places=6, default=0.0, null=True)
    pickup_lat = models.DecimalField(max_digits=9, decimal_places=6, default=0.0, null=True)
    dropoff_lng = models.DecimalField(max_digits=9, decimal_places=6, default=0.0, null=True)
    dropoff_lat = models.DecimalField(max_digits=9, decimal_places=6, default=0.0, null=True)
    trip_price = models.FloatField(default=0, null=True)
    taxi_booking_status = models.CharField(max_length=100, choices=STATUSES)
    trip_distance = models.DecimalField(default=0, null=True, max_digits=9, decimal_places=2)
    description = models.CharField(max_length=500, default='', null=True)
    trip_fare = models.FloatField(default=0)
    duration = models.IntegerField(default=0)
    pickup_datetime = models.DateTimeField(default=timezone.now)
    trip_distance_covered = models.CharField(max_length=255, default='', blank=True)
    booking_time = models.DateTimeField(default=timezone.now)
    cancellation_time = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=255, unique=True)
    accepted_by = models.ForeignKey(Driver, on_delete=models.SET_NULL, blank=True, null=True)



    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.taxi_passenger.user.get_full_name())
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.taxi_passenger.user.get_full_name()}'s Booking - {self.taxi_booking_status} - From '{self.pickup_datetime.strftime('%Y-%m-%d %H:%M')}'"



class MyTrips(models.Model):
    booked_passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    booked_taxi = models.ForeignKey(Taxi, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.booked_passenger.user.get_full_name()}'s Booking - {str(self.booked_taxi)}"
