from django.urls import path

from . import views as store_views

urlpatterns = [
    path('register/', store_views.register, name = 'register_store'),
    path('login/', store_views.login_admin, name = 'login_store'),
    path('dashboard/', store_views.dashboard, name="dashboard" ),
    path('received-orders/', store_views.received_orders, name="received-orders" ),
    path('delivered-orders/', store_views.delivered_orders, name="delivered-orders" ),
    path('add-product/', store_views.add_product, name="add-product" ),
    path('logout-admin/', store_views.logout_admin, name = 'logout-admin'),
    path('edit-product/<int:id>/', store_views.edit_product, name="edit-product" ),
    path('delete-product/<int:id>/', store_views.delete_product, name="delete-product" ),
]