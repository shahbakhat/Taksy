from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views
from core.passenger import views as passenger_views
# from core.driver import views as driver_views, apis as driver_apis
from django.conf.urls.static import static
from django.conf import settings
# from core.views import PassengerLoginView, DriverLoginView,CustomLogoutView
from core.views import home





app_name = 'passenger'
app_name = 'driver'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('sign-up/', views.sign_up, name="sign-up"),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    # Passenegr views
      path('passenger/', include(([
        path('', passenger_views.home, name="passenger-home"),
        path('profile/', passenger_views.profile_page, name="profile"),
        path('payment-method/', passenger_views.payment_method_page, name="payment-method"),
        path('book-a-taxi/', passenger_views.book_taxi_page, name="book-a-taxi"),
        path('my-trips/', passenger_views.my_trips_page, name="my-trips"),
        path('cancel-trip/<uuid:trip_id>/', passenger_views.cancel_trip, name='cancel-trip'),
    ], 'passenger'), namespace='passenger')),

    # Driver views
    # path('driver/', include(([
    #     path('', driver_views.home, name="driver-home"),
    #     path('api/available-trips-api/available/', driver_apis.available_trips_api_page, name="driver-available-trips-api"),
    #     path('trips/driver-home-page/', driver_views.driver_home_page, name="home_page"),
    #     path('trips/driver/trips-view', driver_views.driver_trip_view, name="trip-view"),
    #     path('trips/my-trips/', driver_views.my_jobs_page, name="my-trips"),
    # ], 'driver'), namespace='driver')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)