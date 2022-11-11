from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import Customer, BaseUser
from order_app.models import Order

def signup_page(request):
    return render(request,'user_app/signup.html')

def login_page(request):
    return render(request,'user_app/login.html')

def register_customer(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        password = make_password(request.POST['password'])
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            user=None

        if user:
            message = messages.error(request, "User with provided phone number already exists.")
            return render(request,'user_app/signup.html',{'message':message})

        user = User.objects.create( username=username, 
                                    password=password, 
                                    first_name=first_name, 
                                    last_name=last_name
                                )
        base_user = BaseUser.objects.create(
                                user=user, 
                                role=BaseUser.CUSTOMER,
                                )

        Customer.objects.create(user=base_user)

        return redirect('login')
            
    else:
        return redirect('signup')

def login_user(request):
    if request.method=='POST':
        username = request.POST['username']
        pass_key = request.POST['password']
        user = authenticate(username=username, password=pass_key)
        if user:
            login(request, user)
            return redirect('home_page')
        else:
            return HttpResponse(f"Oops! This user does not exist")


def logout_user(request):
    logout(request)
    return redirect('login')

    
