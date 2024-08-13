from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from l5app.form import UserForm, UserProfileInfoForm

# Create your views here.

def index(request):

    return render(request, 'l5app/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # to save the information to the data-base
            user = user_form.save()   
            # set_password does the hashing of the password
            user.set_password(user.password)
            user.save()

            # commit False to not cause coalisiion with the user.save() from above
            profile = profile_form.save(commit=False) 
            profile.user = user # 1:1 relationship as defined in models.py

            if 'profile_pic' in request.FILES:
                profile.picture = request.FILES['profile_pic']
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'l5app/registration.html', 
                    {
                      'user_form':user_form,
                      'profile_form':profile_form,
                      'registeres':registered
                      }
                    )

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account not active")
        else:
            print("login faled, username: {} and password {}".format(username, password))
            return HttpResponse("invalid login details")
    else:
        return render(request, 'l5app/login.html', {})