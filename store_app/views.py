
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import StoreAdmin, Store
from user_app import models as user_models
from product_app.models import Product
from order_app import models as order_models


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        email = request.POST.get('email','')
        password = request.POST.get('password','')

        phone = request.POST.get('phone','')
        store_name = request.POST.get('store_name','')
        location = request.POST.get('location','')

        user = User.objects.create_user(
            username = username,
            email = email,
            password = password,
        )

        store = Store.objects.create(
            store_name = store_name,
            location = location,
            phone = phone,
        )

        base_user = user_models.BaseUser.objects.create(
            user = user,
            role = user_models.BaseUser.STORE_ADMIN,
        )

        admin = StoreAdmin.objects.create(
            user = base_user,
            store = store
        )



        return redirect('login_store')
        # else:
        #     return render(request, 'store_app/register.html', {'error':'Something went wrong'})

    return render(request, 'store_app/register.html')    
    

def login_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        # admin = StoreAdmin.objects.get(user=user.id)
        admin = user_models.BaseUser.objects.get(user=user.id)
        if admin:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'store_app/login-admin.html', {'error':'Invalid Credentials'})
    else:
        return render(request, 'store_app/login-admin.html')
    
    
def logout_admin(request):
    logout(request)
    return redirect('login-store')

def add_product(request):
    if request.method == 'POST':
        store=user_models.BaseUser.objects.get(user=request.user)
        admin = StoreAdmin.objects.get(user=store)
        if admin.store:
            name = request.POST.get('name')
            price = request.POST.get('price')
            image = request.FILES.get('thumbnail')
            store = admin.store
            product = Product.objects.create(
                name = name,
                unit_price = price,
                image = image,
                store = admin.store,
                slug = store.store_name.replace(' ','-').lower()+'-'+name.replace(' ','-').lower() 
            )
            return redirect('dashboard')
        else: 
            return redirect('login-store')
    else:
        return redirect('dashboard')

# modified by shantosh upload by ashant for store admin panel
def dashboard(request):
    store=user_models.BaseUser.objects.get(user=request.user)
    admin = StoreAdmin.objects.get(user=store)
    products = Product.objects.filter(store=admin.store)
    return render(request, 'store_app/admin-panel.html', {'products':products})

def received_orders(request):
    store=user_models.BaseUser.objects.get(user=request.user)
    admin = StoreAdmin.objects.get(user=store)
    products = Product.objects.filter(store=admin.store)
    orders = order_models.Order.objects.filter(item__in=products, order_status = order_models.Order.ACCEPTED).order_by('-order_date')
    return render(request, 'store_app/received-orders.html', {'orders':orders})

def delivered_orders(request):
    store=user_models.BaseUser.objects.get(user=request.user)
    admin = StoreAdmin.objects.get(user=store)
    products = Product.objects.filter(store=admin.store)
    orders = order_models.Order.objects.filter(item__in=products, order_status = order_models.Order.DELIVERED).order_by('-deliver_date')
    return render(request, 'store_app/delivered-orders.html', {'orders':orders})

def edit_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        image = request.FILES.get('thumbnail')
        if image:
            product.image = image
        product.name = name
        product.unit_price = price
        product.save()
        return redirect('dashboard')
    return render(request, 'store_app/admin-panel.html', {'data':product})

def delete_product(request, id):
    product = Product.objects.get(id=id)
    if product:
        product.delete()

    return redirect('dashboard')
