from django.urls import path
from .views import ProductListView, ProductDetailView,ProductCreateView,ProductUpdateView, ProductDeleteView, CategoryProductListView


app_name = "store"

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete', ProductDeleteView.as_view(), name='product_delete'),
    path('category/<int:category_id>/products/', CategoryProductListView.as_view(), name='category_products')

]