from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from core.passenger import forms
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required(login_url="/login/?next=/passenger/")
def home(request):
    return redirect(reverse('passenger:profile'))


@login_required(login_url="/login/?next=/passenger/")
def profile_page(request):
    user_form = forms.BasicUserForm(instance=request.user)
    passenger_form = forms.BasicCustomerForm(instance=request.user.passenger)
    password_form = PasswordChangeForm(request.user)

    if request.method == "POST":
        if request.POST.get('action') == 'update_profile':

            user_form = forms.BasicUserForm(
                request.POST, instance=request.user)
            passenger_form = forms.BasicCustomerForm(
                request.POST, request.FILES, instance=request.user.passenger)

        if user_form.is_valid() and passenger_form.is_valid():
            user_form.save()
            passenger_form.save()

            # Profile update toast
            messages.success(request, 'profile updated successfully.')
            return redirect(reverse('passenger:profile'))

        elif request.POST.get('action') == 'update_password':
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)


                messages.success(request, 'password updated successfully.')
                return redirect(reverse('passenger:profile'))

    return render(request, 'passenger/profile.html',
                  {"user_form": user_form,
                   "passenger_form": passenger_form,
                   "password_form": password_form,
                   }
                  )

@login_required(login_url="/login/?next=/passenger/payment-method")
def payment_method_page(request):
    current_customer = request.user.passenger
    #saving the payment method
    if not current_customer.stripe_customer_id:
        customer = stripe.Customer.create()
        current_customer.stripe_customer_id = customer['id']
        current_customer.save()
# Get stripe payment method
    stripe_payment_methods = stripe.PaymentMethod.list(
        customer  = current_customer.stripe_customer_id,
        type = "card",)

    print(stripe_payment_methods)

    #Saving lats 4 digits of customer card
    if stripe_payment_methods and len(stripe_payment_methods.data) > 0 :
        payment_method = stripe_payment_methods.data[0]
        current_customer.stripe_payment_method_id = payment_method.id
        current_customer.stripe_card_last4 = payment_method.card.last4
        current_customer.save()
    else:
        current_customer.stripe_payment_method_id = ""
        current_customer.stripe_card_last4 = ""

    # Stripe intent
    intent = stripe.SetupIntent.create(
        customer = current_customer.stripe_customer_id
    )



    return render(request, 'passenger/payment-method.html',
                  {
                    "client_secret":intent.client_secret,
                    "STRIPE_API_PUBLIC_KEY":settings.STRIPE_API_PUBLIC_KEY,
                  }
                  )