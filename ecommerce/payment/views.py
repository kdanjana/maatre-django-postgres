from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.conf import settings

from .models import ShippingAddress, Order, OrderItem
# import cart class
from cart.cart import Cart
from cart.models import CartSummary


# Create your views here.


@login_required(login_url='login')
def checkout(request):
    cart = Cart(request)
    if len(cart) != 0:
        # prefill checkout form if user is logged in 
        # check if user is logged in 
        if request.user.is_authenticated:
            try:
                # check if logged in user has shipping info , return form filled with shipping info
                shipping_address = ShippingAddress.objects.get(user=request.user.id)
                context = {'shipping_address': shipping_address}
                return render(request, 'payment/checkout.html', context)
            except:
                # if logged in user has no shipping info, return blank form
                return render(request, 'payment/checkout.html')
        else:
            # for users who are not registered
            return redirect('register')
    else:
        return redirect('dashboard')



def complete_order(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        shipping_address = (address1 + '\n' + address2 + '\n' + city + '\n' + state + '\n' + country)
        # cart info, accessing shopping cart data
        cart = Cart(request)
        # total price of items in cart
        total_cost = cart.get_total()
        # if user is registered
        order = Order.objects.create(full_name=name, email=email, 
                                        shipping_address=shipping_address,
                                        amount_paid=total_cost,
                                        user=request.user)
        order_id = order.pk
        product_list = []
        for item in cart:
            OrderItem.objects.create(order_id=order_id, product=item['product'],
                                        quantity=item['qty'], price=item['price'],
                                        user=request.user)
            product_list.append(item['product'].title)
        CartSummary.objects.filter(user=request.user).delete()
        prods = ", ".join(product_list)
        send_mail("Order Received", "Hi " + str(name).title() + ", "  + '\n\n' + "Thank you for placing your order." + '\n' 
                  + "You ordered : " + str(prods) + '\n' + "You paid : ₹" + str(cart.get_total()) + '\n' 
                  + "Your products will be delivered within 3 days. ", settings.EMAIL_HOST_USER, [email], fail_silently=False,)
        
    return redirect('payment_success')



def payment_success(request):
    #clear cart
    for key in list(request.session.keys()):
        if key == 'session_key':
            del request.session[key]
    return render(request, 'payment/payment_success.html')



def payment_fail(request):
    return render(request, 'payment/payment_fail.html')