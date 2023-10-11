from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from django.db.models import Q

from .models import Category, Product
# Create your views here.


# store main page
def store(request):
    all_products = Product.objects.all()
    context = {
        'all_products': all_products
    }
    return render(request, 'store/store_front.html', context)


# context processor
def categories(request):
    all_categories = Category.objects.all()
    return {"all_categories": all_categories}


# individual product info page
def product_info(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    context = {"product": product}
    return render(request, "store/product_info.html", context)

# individual category page
def list_category(request, category_slug=None):
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
    all_products = Product.objects.all() 
    if request.method == 'POST':
        product_name = request.POST.get('product_name').capitalize()
        if product_name is not None:
            all_products =  Product.objects.filter(
                 Q(category__name=product_name) |
                 Q(title__icontains=product_name) |
                 Q(description__icontains=product_name) 
            )
            # if product_name is present in title field
            if len(all_products) != 0:
                paginator = Paginator(all_products, 4) # show 4 products per page   
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