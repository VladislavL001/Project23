from django.shortcuts import render

from myproject.store.models import Product


def product_list(request):
    products = Product.objects.all()
    context = {"products":products}
    return render(request, "base.html ")
