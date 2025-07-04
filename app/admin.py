from django.contrib import admin
from .models import Product, Customer

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'reorder_level', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_active', 'size')



@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')

