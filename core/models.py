from django.db import models
from django.contrib.auth.models import User
import uuid
from django.conf import settings
from django.db.models import Sum
from django.shortcuts import reverse
from django.utils import timezone


# Create your models here.
class Passenger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='passenger/pfoile-photos/', blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True)
    stripe_customer_id = models.CharField(max_length=225, blank=True)
    stripe_payment_method_id= models.CharField(max_length=225, blank=True)
    stripe_card_last4 = models.CharField(max_length=225, blank=True)
    def __str__(self):
        return self.user.get_full_name()

# Taxi models
class Taxi (models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    FIVE_SEATER = "5 Seater"
    SEVEN_SEATER = "7 Seater"
    EIGHT_SEATER = "7 Seater"
    TAXI_SIZE = (
        (FIVE_SEATER ,'5 Seater'),
        (SEVEN_SEATER ,' 7 Seater'),
        (EIGHT_SEATER ,' 8 Seater'),
    )
    def __str__(self):
            return self.title

    def get_absolute_url(self):
        return reverse("core:boo-a-taxi", kwargs={
            'slug': self.slug
        })


class BookingStatus(models.Model ):

    BOOKING_STATUS = 'booking in proccess'
    BOOKED_STATUS = 'booked'
    TAXI_ARRIVED = 'arrived'
    PASSENGER_ONBOAD = 'onboard'
    TRIP_COMPLETED = 'complete'
    TRIP_CANCELLED = 'cancelled'
    STATUSES = (
        (BOOKING_STATUS,'Booking in process'),
        (TAXI_ARRIVED,'Arrived'),
        (BOOKED_STATUS , 'booked'),
        (PASSENGER_ONBOAD , 'You are on board'),
        (TRIP_CANCELLED , 'Trip has been canceled'),
        (TRIP_COMPLETED , 'Trip has been completed')

    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booked = models.BooleanField(default=False)
    taxi = models.ForeignKey(Taxi, on_delete=models.CASCADE)


    def __str__(self):
        return self.user

class BookingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    pickup_address = models.CharField(max_length=255, blank=False)
    dropoff_address = models.CharField(max_length=255, blank=False)
    pickup_longitude = models.FloatField()
    pickup_latitude = models.FloatField()

    def __str__(self):
        return self.user.username
