from django.shortcuts import render , redirect
from django .contrib.auth  import login
from django.contrib.auth.decorators import login_required

from . import forms
# Create your views here.
def home(request):
    return render (request, 'home.html')

@login_required()
def passenger_page(request):
    return render (request, 'home.html')
@login_required()
def driver_page(request):
    return render (request, 'home.html')


def sign_up(request):
    form = forms.SignUpForm()

    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()

            user =form.save(commit=False)
            user.username = email
            user.save()


            login(request,user)
            return redirect('/')

    return render(request, 'sign-up.html', {'form': form
                                            })
