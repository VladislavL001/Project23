from django.urls import path
from .views import product_list, products_detail


app_name = "store"

urlpatterns = [
    path('', product_list, name='product_list'),
    path('product/<int:pk>/', products_detail, name='products_detail')
]