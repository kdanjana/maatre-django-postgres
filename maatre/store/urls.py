
from django.urls import path

from . import views

urlpatterns = [
    # store main page
    path("", views.store, name="store"),
    # individual product info page
    path("product/<slug:product_slug>", views.product_info, name="product_info"),
    # individual category page
    path("search/<slug:category_slug>",views.list_category, name='list_category'),
    path("all_products", views.all_products, name='all_products'),
]
