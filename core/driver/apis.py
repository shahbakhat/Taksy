from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from core.models import *

@csrf_exempt
@login_required(login_url="/drive/login")
def available_trips_api_page(request):
    available_trips = list(Taxi.objects.filter(taxi_booking_status=Taxi.TRIP_BOOKED).values())
    return JsonResponse(
        {
            "success":True,
            "available_trips":available_trips,
        }
    )