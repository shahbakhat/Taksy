from django.contrib import admin
from . import  models
# Register your models here.
admin.site.register(models.Passenger)
admin.site.register(models.Taxi)
admin.site.register(models.BookingStatus)
admin.site.register(models.BookingAddress)
