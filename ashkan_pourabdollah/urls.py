"""
URL configuration for ashkan_pourabdollah project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from clothes_app.views import *
from django.conf.urls.static import static
from django.conf import settings
from azbankgateways.urls import az_bank_gateways_urls


urlpatterns = [
    path('admin/', admin.site.urls),

    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('about/', about, name="about"),
    path('search/', search, name="search"),
    path('contact/', contact, name="contact"),
    path('signIn/', signIn, name="signin"),
    path('logIn/', logIn, name='login'),
    path('logOut/', logOut, name="logout"),
    path('products/', products, name="products"),
    path('single-product/<product>/', single_product, name="single-product"),
    path('cart/', cart, name="cart"),
    path('user/', userPage, name="user"),
    path('deleteCart/<productID>/', deleteCart, name="deleteCart"),
    path('invoice/',invoiceItem,name="invoice"),

    path('api/hexa/',include('clothes_api.urls')),
    
    path('payment/', go_to_gateway_view),
    path('bankgateways/', az_bank_gateways_urls()),
    path('callback-gateway', callback_gateway_view)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)