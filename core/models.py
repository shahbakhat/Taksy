from django.db import models
from django.contrib.auth.models import User


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

