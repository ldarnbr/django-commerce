from django.contrib import admin
from .models import Item, ShoppingBasket, BasketItem, Order, OrderItem
# https://docs.djangoproject.com/en/6.0/intro/tutorial07/
# Adjusted to present lists in admin view showing relevant information for each db table.
# Register your models here.

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock_count', 'sale_discount')

@admin.register(ShoppingBasket)
class ShoppingBasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer')

@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'basket', 'item', 'quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_date', 'id', 'customer')
    list_filter = ('order_date',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'item', 'quantity', 'price')