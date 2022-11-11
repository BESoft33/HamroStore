from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms


from user_app.models import Customer, BaseUser

    
admin.site.register(Customer)


admin.site.register(BaseUser)
# admin.site.register(Customer)