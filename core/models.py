from django.db import models
from django.contrib.auth.models import User
import uuid
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

# Taxi category models
class TaxiCategory(models.Model):
    slug = models.CharField(max_length=225, unique=True)
    FIVE_SEATER = "5 Seater"
    SEVEN_SEATER = "7 Seater"
    EIGHT_SEATER = "7 Seater"
    TAXI_SIZE = (
        (FIVE_SEATER ,'5 Seater'),
        (SEVEN_SEATER ,' 7 Seater'),
        (EIGHT_SEATER ,' 8 Seater'),
        )
    name  = models.CharField(max_length=20, choices= TAXI_SIZE,default= FIVE_SEATER)

    def __str__(self):
        return self.name



# Trip model

class TripStatus(models.Model ):
    BOOKING_STATUS = 'booking in proccess'
    TAXI_ARRIVED = 'arrived'
    PASSENGER_ONBOAD = 'onboard'
    TRIP_COMPLETED = 'complete'
    TRIP_CANCELLED = 'cancelled'
    STATUSES = (
        (BOOKING_STATUS,'Booking in process'),
        (TAXI_ARRIVED,'arrived'),
        (PASSENGER_ONBOAD , 'Passenger on board'),
        (TRIP_CANCELLED , 'Trip has been canceled'),
        (TRIP_COMPLETED , 'Trip has been completed')

    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Passenger, on_delete=models.CASCADE )
    name = models.CharField(max_length=225)
    status = models.CharField(max_length=20, choices= STATUSES,default= BOOKING_STATUS)
    created_at = models.DateTimeField(default= timezone.now )
    def __str__(self):
            return self.name


