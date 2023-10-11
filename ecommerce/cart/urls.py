
from django.urls import path

from . import views

urlpatterns = [
    # cart main page
    path("", views.cart_summary, name="cart_summary"),
    # adding to cart page
    path("add/", views.cart_add, name="cart_add"),
    # deleting from cart  page
    path("delete/", views.cart_delete, name="cart_delete"),
    # updating cart page
    path("update/", views.cart_update, name="cart_update"),    
    path('saveitems_cart/', views.saveitems_cart, name="saveitems_cart"),
]
