from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

from .cart import Cart
from .models import CartSummary
from store.models import Product



# cart main page
def cart_summary(request):
   return render(request, "cart/cart_summary.html")


# adding to cart
def cart_add(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('selection'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, product_qty=product_quantity)
        return HttpResponseRedirect(reverse("store"))



# deleting from cart 
def cart_delete(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        return HttpResponseRedirect(reverse("cart_summary"))
    


def total_items(request):
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
    user= request.user.id 
    # get items in cart for that user
    CartSummary.objects.filter(user_id=user).delete()
    for product in cart:
        prod_id = product['id']
        CartSummary.objects.create(user_id=user, product_id=prod_id,qty=product['qty'])
    
    return redirect('dashboard')
