from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

from .cart import Cart
from .models import CartSummary
from store.models import Product



def cart_summary(request):
    """ displays cart"""
    return render(request, "cart/cart_summary.html")


def cart_add(request):
    """ adding product to cart"""
    cart = Cart(request)
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('selection'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, product_qty=product_quantity)
        return HttpResponseRedirect(reverse("store"))



def cart_delete(request):
    """ deleting product from cart"""
    cart = Cart(request)
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        return HttpResponseRedirect(reverse("cart_summary"))
    


def total_items(request):
    """ count the total number of products present in cart"""
    cart = Cart(request)
    return {"total_qty": len(cart)}




# updating cart
def cart_update(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('selection'))
        cart.update(product=product_id, qty=product_quantity)
        return HttpResponseRedirect(reverse("cart_summary"))

  
        
@login_required(login_url='login')
def saveitems_cart(request):
    cart = Cart(request)
    if len(cart) != 0:
        user= request.user.id 
        # get items in cart for that user
        CartSummary.objects.filter(user_id=user).delete()
        for product in cart:
            prod_id = product['product'].id
            CartSummary.objects.create(user_id=user, product_id=prod_id,qty=product['qty'])
    return redirect('dashboard')
