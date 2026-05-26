from django.conf import settings
from django.core.cache import cache

from store.models import Product


def get_products_from_cache():
    if not settings.CACHE_ENABLED:
        return Product.objects.all()
    key = "products_list"
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products)
    return products