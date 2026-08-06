from django.db import models
# https://docs.djangoproject.com/en/6.0/ref/contrib/auth/
from django.contrib.auth.models import User

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    stock_count = models.IntegerField(default=0)
    # Selling items only under £1000.00 so 5 max digits is enough.
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # Sale discount is represented as a decimal i.e. 10% off = 0.10
    sale_discount = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class ShoppingBasket(models.Model):
    # Customers have one basket, which should be deleted if the customer account
    # is removed.
    customer = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Belongs to: {self.customer.username}"

class BasketItem(models.Model):
    # All basket items link to an item class. If the item is removed, delete the
    # instances of the items in users baskets.
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    basket = models.ForeignKey(ShoppingBasket, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    # https://stackoverflow.com/questions/8016412/in-django-do-models-have-a-default-timestamp-field
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    # Price fluctuations shouldn't change price of item in the order.
    # Need to hard set this rather than reading from current pricing.
    price = models.DecimalField(max_digits=5, decimal_places=2)