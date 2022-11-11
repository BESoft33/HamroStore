from django.shortcuts import render

from .models import Product
from user_app.models import Customer
from order_app.models import Order
from store_app.models import Store


def home_page(request):

    products = Product.objects.all()

    return render(request, 'product_app/products.html', {'products': products})







