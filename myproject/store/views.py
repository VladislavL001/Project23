from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProductForm
from .models import Product


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("store:product_list")


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_form.html'
    success_url = reverse_lazy("store:product_list")


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'store/product_confirm_delete.html'
    success_url = reverse_lazy("store:product_list")