from urllib.request import CacheFTPHandler
from django.contrib import admin

from .models import Order, Cart, BillingLocation

admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(BillingLocation)


