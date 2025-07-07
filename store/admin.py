from django.contrib import admin
from .models import Product, CartItem, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered', 'ordered_date']
    list_filter = ['ordered', 'ordered_date']
