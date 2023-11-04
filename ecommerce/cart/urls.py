
from django.urls import path

from . import views

urlpatterns = [
    # cart main page
    path("", views.cart_summary, name="cart_summary"),
    # adding to cart 
    path("add/", views.cart_add, name="cart_add"),
    # deleting from cart  
    path("delete/", views.cart_delete, name="cart_delete"),
    # updating cart 
    path("update/", views.cart_update, name="cart_update"),    
    # saving items present in cart
    path('saveitems_cart/', views.saveitems_cart, name="saveitems_cart"),
]
