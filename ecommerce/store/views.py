from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from django.db.models import Q

from .models import Category, Product
# Create your views here.


def store(request):
    """ maatre store's main page"""
    all_products = Product.objects.all()
    context = {
        'all_products': all_products
    }
    return render(request, 'store/store_front.html', context)


# context processor
def categories(request):
    """ all_categories - can be accessed from anywhere in template"""
    all_categories = Category.objects.all()
    return {"all_categories": all_categories}



def product_info(request, product_slug):
    """ to get all info about a single product """
    product = get_object_or_404(Product, slug=product_slug)
    context = {"product": product}
    return render(request, "store/product_info.html", context)



def list_category(request, category_slug=None):
    """ to get all products of a category"""
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    paginator = Paginator(products, 4) # show 4 products per page   
    page_number = request.GET.get("page")
    page_ob = paginator.get_page(page_number)
    context = {
        "products": page_ob,
        "category": category
    }
    return render(request, "store/list_category.html", context)



def all_products(request):  
    """ displays all products(get),can search for a product(post)"""
    all_products = Product.objects.all() 
    if request.method == 'POST':
        product_name = request.POST.get('product_name').capitalize()
        if product_name is not None:
            all_products =  Product.objects.filter(
                 Q(category__name=product_name) |
                 Q(title__icontains=product_name) |
                 Q(description__icontains=product_name) 
            )
            if len(all_products) != 0:
                paginator = Paginator(all_products, 4) 
                page_number = request.GET.get("page")
                page_ob = paginator.get_page(page_number)
                return render(request, 'store/all_products.html', {'all_products': page_ob})
            else:
                context = {'error': 'Invalid search item'}
                return render(request, 'store/all_products.html', context)
    paginator = Paginator(all_products, 4) # show 4 products per page   
    page_number = request.GET.get("page")
    page_ob = paginator.get_page(page_number)
    return render(request, 'store/all_products.html', {'all_products': page_ob})


def custom_404(request, exception):
    return render(request, '404.html')
