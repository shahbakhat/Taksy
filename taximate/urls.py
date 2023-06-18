from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views
from core.passenger import views as passenger_views
from core.driver import views as driver_views, apis as driver_apis
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path('sign-up/', views.sign_up, name="sign-up"),
    # Passenegr views
      path('passenger/', include(([
        path('', passenger_views.home, name="passenger-home"),
        path('profile/', passenger_views.profile_page, name="passenger-profile"),
        path('payment-method/', passenger_views.payment_method_page, name="passenger-payment-method"),
        path('book-a-taxi/', passenger_views.book_taxi_page, name="passenger-book-a-taxi"),
        path('my-trips/', passenger_views.my_trips_page, name="passenger-my-trips"),
        path('cancel-trip/<uuid:trip_id>/', passenger_views.cancel_trip, name='passenger-cancel-trip'),
    ], 'passenger'), namespace='passenger')),

    # Driver views
    path('driver/', include(([
        path('', driver_views.home, name="driver-home"),
        path('api/available-trips-api/available/', driver_apis.available_trips_api_page, name="driver-available-trips-api"),
        path('trips/available/', driver_views.available_trips_page, name="driver-available-trips"),
        path('trips/available/my-jobs/', driver_views.my_jobs_page, name="driver-my-jobs"),
    ], 'driver'), namespace='driver')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
