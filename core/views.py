from django.urls import reverse_lazy
from .models import User,TaxiPassenger,TaxiDriver,Driver,Passenger
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from . import forms
from django.contrib.auth import get_user_model, logout ,authenticate, login
from django.db import transaction
from django.urls import reverse
from .forms import PassengerSignUpForm
from .models import Passenger



def home(request):
    return render(request, 'welcome.html')


User = get_user_model()




def sign_up(request):
    passenger_signup_form = PassengerSignUpForm()

    if request.method == 'POST':
        form = PassengerSignUpForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                email=form.cleaned_data['email'],
                username=form.cleaned_data['email'],  # Use the email as the username
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                role=User.Role.TAXIPASSENGER
            )

            passenger = Passenger(user=user)
            # Update passenger fields here
            passenger.save()

            # Authenticate and log in the user
            user = authenticate(request, username=user.email, password=form.cleaned_data['password'])
            login(request, user)

            messages.success(request, "You have successfully signed up as a passenger.")
            return redirect('passenger:book-a-taxi')  # Replace 'home' with the desired URL after login

    return render(request, 'sign-up.html', {
        'passenger_signup_form': passenger_signup_form,
    })








# class CustomLogoutView(TemplateView):
#     template_name = 'welcome.html'

#     def dispatch(self, request, *args, **kwargs):
#         logout(request)
#         return render(request, 'welcome.html')


# class PassengerLoginView(LoginView):
#     template_name = 'registration/passenger-login.html'
#     success_url = ('passenger:profile')

# class DriverLoginView(LoginView):
#     template_name = 'registration/driver-login.html'
#     success_url = reverse_lazy('driver:trip-view')



# def sign_up(request):
#     passenger_signup_form = forms.PassengerSignUpForm()
#     driver_signup_form = forms.DriverSignUpForm()

#     if request.method == 'POST':
#         form_type = request.POST.get('form_type')

#         if form_type == 'passenger_signup':
#             form = forms.PassengerSignUpForm(request.POST)
#             role = get_user_model().Role.TAXIPASSENGER
#         elif form_type == 'driver_signup':
#             form = forms.DriverSignUpForm(request.POST)
#             role = get_user_model().Role.TAXIDRIVER
#         else:
#             form = None
#             role = None

#         if form and form.is_valid():
#             with transaction.atomic():
#                 user = get_user_model().objects.create_user(
#                     email=form.cleaned_data['email'],
#                     username=form.cleaned_data['email'],  # Use the email as the username
#                     password=form.cleaned_data['password'],
#                     first_name=form.cleaned_data['first_name'],
#                     last_name=form.cleaned_data['last_name'],
#                     role=role
#                 )

#                 if role == get_user_model().Role.TAXIPASSENGER:
#                     passenger = Passenger(user=user)
#                     # Update passenger fields here
#                     passenger.save()

#                     messages.success(request, "You have successfully signed up as a passenger.")
#                     return redirect('passenger-login')
#                 elif role == get_user_model().Role.TAXIDRIVER:
#                     driver = Driver(user=user)
#                     # Update driver fields here
#                     driver.save()

#                     messages.success(request, "You are already registered as a driver. Please log in.")
#                     return redirect('driver-login')
#                 else:
#                     form = None
#                     role = None
#                     messages.error(request, "Unfortunately, an error occurred. Please try again.")
#                     return redirect('sign-up')

#     return render(request, 'sign-up.html', {
#         'passenger_signup_form': passenger_signup_form,
#         'driver_signup_form': driver_signup_form,
#     })