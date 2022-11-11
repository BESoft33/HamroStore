from uuid import uuid4
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Order, Cart, BillingLocation
from product_app.models import Product
from product_app.views import home_page
from user_app.models import Customer, BaseUser


@login_required
def orders(request):
    customer = Customer.objects.get(user=BaseUser.objects.get(user=request.user))
    orders = Order.objects.filter(user=customer).exclude(order_status__in=(Order.CANCELLED, Order.DELIVERED))
    total = sum([Product.objects.get(id=order.item_id).unit_price*order.quantity for order in orders])
    return render(request, 'order_app/orders.html', {'orders': orders, 'total': total})

@login_required
def cart(request):
    customer = Customer.objects.get(user=BaseUser.objects.get(user=request.user))
    cart = Cart.objects.filter(user=customer)
    
    return render(request, 'order_app/cart.html', {'carts': cart})

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    user = Customer.objects.get(user=BaseUser.objects.get(user=request.user))
    cart,created = Cart.objects.get_or_create(user=user, item=product)
    if created:
        cart.save()
    return redirect(home_page)

@login_required
def delete_from_cart(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    if cart:
        cart.delete()
    return redirect('cart')

@login_required
def order_all(request):
    customer = Customer.objects.get(user=BaseUser.objects.get(user=request.user))
    cart = Cart.objects.filter(user_id=customer.id)
    orders = Order.objects.filter(user_id=customer.id, order_status=Order.PENDING)
    order_ids = [order.item_id for order in orders]
    request_id = uuid4().hex[:16].upper()
    for item in cart:
        if not item.item_id in order_ids:
            Order.objects.create(user=customer, item_id=item.item_id, quantity=1, request_id=request_id)

    return redirect('orders')

@login_required
def order_item(request, product_id):
    product = Product.objects.get(id=product_id)
    # print(request.user)
    base_user = BaseUser.objects.get(user=request.user)
    print(base_user)
    user = Customer.objects.get(user=base_user)
    request_id = uuid4().hex[:16].upper()
    order = Order.objects.create(user=user, item=product, quantity=1, request_id=request_id)
    if order:
        order.save()
    return render(request, 'order_app/checkout.html', {'orders': [order]})


@login_required
def delete_from_orders(request, order_id):
        order = Order.objects.get(id=order_id)

        if order and not order.order_status==order.ACCEPTED:
            order.order_status = order.CANCELLED
            order.save()
        return redirect('orders')

@login_required
def orders(request):
    customer = Customer.objects.get(user=BaseUser.objects.get(user=request.user))
    orders = Order.objects.filter(user= customer).exclude(order_status__in=(Order.CANCELLED, Order.DELIVERED))
    return render(request, 'order_app/orders.html', {'orders': orders})

@login_required
def checkout(request):
    customer = Customer.objects.get(user=BaseUser.objects.get(user=request.user))
    orders = Order.objects.filter(user_id=customer, order_status=Order.PENDING)
    total_orders = len(orders)
    quantities = [request.POST.get(f'quantity-{order.id}') for order in orders]

    for order, quantity in zip(orders, quantities):
        order.quantity = quantity
        order.save()
    
    total = sum([Product.objects.get(id=order.item_id).unit_price*float(order.quantity) for order in orders])
    data =  {
        'orders': orders, 
        'total_orders': total_orders, 
        'total': total,
        'quantities': quantities
    }
    
    return render(request, 'order_app/checkout.html',data)

@login_required
def billing_location_form(request):
    customer = Customer.objects.get(user=BaseUser.objects.get(user=request.user))

    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        address = request.POST.get('address')
        email = request.POST.get('email')
        
        orders = Order.objects.filter(user_id=customer, order_status=Order.PENDING)
        if orders:
            location = BillingLocation.objects.create(
                                request_id=orders[0].request_id,
                                first_name=first_name, 
                                last_name=last_name, 
                                address=address, 
                                email=email)
            if location:
                for order in orders:
                    order.order_status = Order.ACCEPTED
                    order.save()
            
            return redirect('orders')
        
        return redirect('/')
    else:
        return render(request, 'order_app/billing_address.html',{'customer':customer})


def verify_payment(request):

    id = request.GET.get('amount')
    
    if id:
        return JsonResponse({"success":True})
    return JsonResponse({'success':False})

@login_required
def mark_as_delivered(request, order_id):
    order = Order.objects.get(id=order_id)
    if order:
        order.order_status = Order.DELIVERED
        order.save()
    return redirect('accepted_orders')

@login_required
def accepted_orders(request):
    customer = Customer.objects.get(user=BaseUser.objects.get(user=request.user))
    orders = Order.objects.filter(user_id=customer, order_status=Order.ACCEPTED)
    return render(request, 'order_app/receive-order.html', {'orders': orders})
