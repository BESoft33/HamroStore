from django.contrib import admin
from django.urls import path
from . import views as user_views

urlpatterns = [
    path('signup/',user_views.signup_page, name='signup'),
    path('login/',user_views.login_page, name='login'),
    path('logout/', user_views.logout_user, name='logout'),
    path('register/',user_views.register_customer, name='register'),
    path('authenticate/',user_views.login_user, name='authenticate'),    
]
