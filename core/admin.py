from django.contrib import admin
from . import  models

from django.contrib.auth import get_user_model

User = get_user_model()
admin.site.register(User)
# Register your models here.
admin.site.register(models.Passenger)
admin.site.register(models.Taxi)
admin.site.register(models.MyTrips)
admin.site.register(models.Driver)





