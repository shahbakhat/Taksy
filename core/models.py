from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Passenger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_avatar = models.ImageField(upload_to='passenger/avatar/', blank=True, null=True)
    def __str__(self):
        return self.user.get_full_name()

