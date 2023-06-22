from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from core import views as core_views
from core.passenger import views as passenger_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'),
    path('sign-up/', core_views.sign_up, name="sign-up"),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    
    # Passenger views
    path('passenger/', include(([
        path('', passenger_views.home, name="passenger-home"),
        path('profile/', passenger_views.profile_page, name="profile"),
        path('payment-method/', passenger_views.payment_method_page, name="payment-method"),
        path('book-a-taxi/', passenger_views.book_taxi_page, name="book-a-taxi"),
        path('my-trips/', passenger_views.my_trips_page, name="my-trips"),
        path('cancel-trip/<uuid:trip_id>/', passenger_views.cancel_trip, name='cancel-trip'),
    ], 'passenger'), namespace='passenger')),
    
    # Other URL patterns
    
]

# Append the following line to include static files in development
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
