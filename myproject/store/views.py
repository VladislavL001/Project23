from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProductForm, ProductModeratorsForm
from .models import Product
from django.utils.decorators import method_decorator

from .services import get_products_from_cache


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'

    def get_queryset(self):
        return get_products_from_cache()


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("store:product_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_form.html'
    success_url = reverse_lazy("store:product_list")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm("store.can_unpublish_product") and user.has_perm("store.delete_product"):
            return ProductModeratorsForm
        raise PermissionDenied



class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'store/product_confirm_delete.html'
    success_url = reverse_lazy("store:product_list")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm("store.can_unpublish_product") and user.has_perm("store.delete_product"):
            return ProductModeratorsForm
        raise PermissionDenied