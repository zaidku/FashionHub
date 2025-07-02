from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views

urlpatterns = [
    # Original URLs
    path('', views.dashboard, name='home'),  # Changed from views.home to views.dashboard
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    
    # Inventory System URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('inventory/', views.inventory, name='inventory'),
    path('sales/', views.sales, name='sales'),
    path('accounting/', views.accounting, name='accounting'),
    path('settings/', views.settings, name='settings'),
    path('inventory/add/', views.add_product, name='add_product'),
    
    # Authentication URLs
    path('login/',
         LoginView.as_view(
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context={
                 'title': 'Log in',
                 'year': datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]