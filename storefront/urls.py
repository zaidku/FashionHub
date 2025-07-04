#storefront/urls.py

from django.urls import path
from . import views

app_name = 'storefront'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/<slug:slug>/order/', views.place_order, name='place_order'),
    
    # Cart URLs
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<slug:slug>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<slug:slug>/', views.update_cart, name='update_cart'),
    
    # Checkout URL
    path('checkout/', views.checkout, name='checkout'),
]