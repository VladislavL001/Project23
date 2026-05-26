from django.conf import settings
from django.core.cache import cache

from store.models import Product


def get_products_from_cache():
    """Кеширование списка продуктов"""
    if not settings.CACHE_ENABLED:
        return Product.objects.all()
    key = "products_list"
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products)
    return products


def get_products_by_category(category_id):
    """Возвращает опубликованные товары выбранной категории."""

    if not settings.CACHE_ENABLED:
        return Product.objects.filter(
            category_id=category_id,
            is_published=True
        ).select_related("category")

    key = f'category_{category_id}'

    products = cache.get(key)

    if products is None:
        products = list(
            Product.objects.filter(
                category_id=category_id,
                is_published=True
            ).select_related("category")
        )

        cache.set(key, products, 60 * 15)

    return products