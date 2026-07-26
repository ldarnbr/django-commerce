from django.contrib import admin
from .models import Item, ShoppingBasket, BasketItem, Order, OrderItem
# https://docs.djangoproject.com/en/6.0/intro/tutorial07/
# Register your models here.

admin.site.register(Item)
admin.site.register(ShoppingBasket)
admin.site.register(BasketItem)
admin.site.register(Order)
admin.site.register(OrderItem)
