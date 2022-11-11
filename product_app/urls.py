from django.contrib import admin
from django.urls import path

from . import views as product_views


urlpatterns = [
    path('', product_views.home_page, name='home_page'),
    

]
