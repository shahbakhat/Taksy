from django.shortcuts import render, redirect
# from .forms import DriverSignUpForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# from core.models import Driver



# @login_required(login_url="/login/?next=/driver/")


# def driver_signup(request):
#     if request.method == 'POST':
#         form = DriverSignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False  # Set user as inactive until verified by admin
#             user.save()

#             driver = Driver.objects.create(user=user, phone_number=form.cleaned_data['phone_number'])

#             # Perform any additional actions or redirect as needed

#             return redirect('login')  # Redirect to login page after successful sign-up
#     else:
#         form = DriverSignUpForm()

#     return render(request, 'driver_signup.html', {'form': form})
@login_required(login_url="/login/?next=/driver/")
def home(request):
    return render(request, '/drivers/home.html')
