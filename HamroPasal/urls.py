
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from product_app import views as product_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('product_app.urls')),
    path('user_app/',include('user_app.urls')),
    path('store_app/', include('store_app.urls')),
    path('order_app/', include('order_app.urls')),

    path('khalti/', include('khalti.urls')),


]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)