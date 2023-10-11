from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return self.name
    
    # to build a dynamic url
    def get_absolute_url(self):
        return reverse("list_category", args=[self.slug])
    


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='product')
    title = models.CharField(max_length=200)
    brand = models.CharField(max_length=200, default="un-branded")
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='images/')

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self) -> str:
        return self.title
    
    # to build a dynamic url
    def get_absolute_url(self):
        return reverse("product_info", args=[self.slug])
    

