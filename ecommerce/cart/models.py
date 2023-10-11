from django.db import models

from store.models import Product
from django.contrib.auth.models import User

# Create your models here.
class CartSummary(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qty = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Cart Summary'


    def __str__(self):
        return f" {self.user} : {self.product} "
