from django.db import models
from django.contrib.auth.models import User

from store.models import Product


# Create your models here.

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
                                # null=true beacuse registered or non registered can use shipping address
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=255)
    address1 = models.CharField(max_length=500)
    address2 = models.CharField(max_length=500)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200, null=True, blank=True)# null=true-->tells db it iso k to leave this field empty,
                                # blank=true tells client it is ok to not enter this while filling form
    country = models.CharField(max_length=200, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self) -> str:
        return 'Shipping Address - ' + str(self.id)
    


class Order(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=255)
    shipping_address = models.TextField(max_length=1000)
    # total quantity of user's order
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    # automatically set as soon as record is created
    date_ordered = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return 'Order: ' + str(self.id)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # number of items  per product present in user's order i.e will be 4 if user purchased 4 black jeans
    # product will contain info of black jeans stored in Product model
    # price will total price of 4 black jeans
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return 'Order Item: ' + str(self.id)



