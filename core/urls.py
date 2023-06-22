from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sign-up/', views.sign_up, name='sign-up'),
    # Add other URL patterns for core app
]
from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sign-up/', views.sign_up, name='sign-up'),
    # Add other URL patterns for core app
]
