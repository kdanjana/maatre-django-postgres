from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from .forms import CreateUserForm, LoginForm, UpdateUserForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress

from cart.cart import Cart
from store.models import Product
from cart.models import CartSummary
from payment.models import Order, OrderItem

# it will collect ur hosts domain name if u r hosting this app on elastic beanstalk
# since we ar running this on local pc this will be 127.0.0.1:8000
from django.contrib.sites.shortcuts import get_current_site


from .token_generator import user_tokenizer_generate

# used for setting up the markup  for email verification link 
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str

# we want to decode token generator so it will be usabel and encode token generator when we are sending it
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.contrib.auth.models import auth     # auth allows us to do authentication
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.


def register(request):
    """ registration page"""
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # we want any one that registers  to have their account deactivated without having 
            # email verification done first  so we , change users's active status to false
            user.is_active = False  # deactivate users account
            user.save()
            # email verification set up 
            current_site = get_current_site(request)
            subject = "Maatre account verification email."
            message = render_to_string("account/registration/email_verification.html",{
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': user_tokenizer_generate.make_token(user),                                    
            })
            user.email_user(subject=subject, message=message)
            return redirect('email_verification_sent')
    context = {'form': form}
    return render(request, "account/registration/register.html", context)


def email_verification(request, uidb64, token):
    user_id = force_str(urlsafe_base64_decode(uidb64))      # decode user id 
    user = User.objects.get(pk=user_id)
    # success i.e if user clicked on the link sent to his email then its a success
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True                               # activate users account
        user.save()     
        return redirect('email_verification_success')
    else:
        return redirect('email_verification_fail')


def email_verification_sent(request):
    return render(request, 'account/registration/email_verification_sent.html')

def email_verification_success(request):
    return render(request, 'account/registration/email_verification_success.html')

def email_verification_fail(request):
    return render(request, 'account/registration/email_verification_fail.html')


def login(request):
    """ login page"""
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data = request.POST)
        if form.is_valid():
            username_form = request.POST.get('username')
            password_form = request.POST.get('password')
            # do authentication i.e compare username and pwd from db to form's username and pwd
            user = authenticate(request, username=username_form, password=password_form)
            if user is not None:                # if user exists in db
                auth.login(request, user)       # allow user to login
                cart = Cart(request)
                allitems = CartSummary.objects.filter(user_id=request.user.id)
                if len(allitems) != 0:
                    for item in allitems:
                        product = Product.objects.get(id=str(item.product_id))
                        cart.add(product, item.qty)
                return redirect('dashboard')
    context = {'form': form}
   
    return render(request, 'account/login.html', context)
            


def logout(request):
    cart = Cart(request)
    user= request.user.id 
    # get items in cart for that user
    CartSummary.objects.filter(user_id=user).delete()
    if len(cart) != 0:        
        for product in cart:
            prod_id = product['product'].id
            CartSummary.objects.create(user_id=user, product_id=prod_id,qty=product['qty'])       
    cart.del_session(request)
    auth.logout(request)
    messages.success(request, "Logout success!")
    return redirect('store')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'account/dashboard.html')


@login_required(login_url='login')
def profile_management(request):
    """ updating user's username and email"""
    form = UpdateUserForm(instance=request.user)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)  # capture post request  of all data  based on instance of current user i.e user currently signed in 
        if form.is_valid():
            form.save()
            messages.info(request, 'Account updated!')
            return redirect('dashboard')   
    return render(request, 'account/profile_management.html', {'form': form})



@login_required(login_url='login')
def delete_account(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.delete()
        messages.error(request, 'Account Deleted!')
        return redirect('store')
    return render(request, 'account/delete_account.html')



# payment view
@login_required(login_url='login')
def manage_shipping(request):
    try:
        # check if logged in user already has shipping info 
        shipping_address = ShippingAddress.objects.get(user=request.user.id) 
    except ShippingAddress.DoesNotExist:
        # if logged in user doesnt have shipping info stored in shippingaddress model
        shipping_address = None
    form = ShippingForm(instance=shipping_address)
    if request.method == "POST":
        form = ShippingForm(request.POST, instance=shipping_address)
        if form.is_valid():
            shipping_user = form.save(commit=False)
            shipping_user.user = request.user
            shipping_user.save()
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'account/shipping.html', context)


@login_required(login_url='login')
def track_orders(request):
    try:
        orders = OrderItem.objects.filter(user=request.user)
        context = {'orders': orders}
        return render(request, 'account/track_orders.html', context)    
    except:
        return render(request, 'account/track_orders.html')
