from django.urls import path
from core import views
from django.urls import path, include
from . import views
from core.passenger import views as passenger_views

urlpatterns = [
    path('', views.home, name='home'),
    path('sign-up/', views.sign_up, name='sign-up'),
    # Add other URL patterns for core app

    # Add the passenger app patterns
    path('passenger/', include((
        [
            path('', passenger_views.home, name="passenger-home"),
            path('profile/', passenger_views.profile_page, name="profile"),
            path('payment-method/', passenger_views.payment_method_page, name="payment-method"),
            path('book-a-taxi/', passenger_views.book_taxi_page, name="book-a-taxi"),
            path('my-trips/', passenger_views.my_trips_page, name="my-trips"),
            path('cancel-trip/<uuid:trip_id>/', passenger_views.cancel_trip, name='cancel-trip'),
        ],
        'passenger'
    ), namespace='passenger')),
]

