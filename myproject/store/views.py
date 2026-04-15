from .models import Product
from django.views.generic import ListView, DetailView


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'