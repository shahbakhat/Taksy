from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from core.models import Passenger,Taxi
# from django.forms import ModelForm


class BasicUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class BasicCustomerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ('profile_photo', 'phone_number')

class TaxiBookingForm(forms.ModelForm):
    pickup_address = forms.CharField(max_length=255,required=True,label='',
                                      widget= forms.TextInput
                           (attrs={'placeholder':'Where are you?',
                                   })
                                     )
    dropoff_address = forms.CharField(max_length=255, required=True,label='',
                                      widget= forms.TextInput
                           (attrs={'placeholder':'Where you want to go?',
                                   }))
    pickup_lng = forms.FloatField(required=False, )
    pickup_lat = forms.FloatField(required=False, )
    dropoff_lng = forms.FloatField(required=False, )
    dropoff_lat = forms.FloatField(required=False, )

    class Meta:
        model = Taxi
        fields = ('pickup_address','pickup_lng','pickup_lat','dropoff_address','dropoff_lat','dropoff_lng', 'taxi_size')




