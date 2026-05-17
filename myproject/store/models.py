from django.db import models
from django.conf import settings

class Category(models.Model):
    """Модель категории товаров"""

    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(
        verbose_name="Описание",
        blank=True,  # Поле может быть пустым
        null=True,  # Разрешить NULL в базе данных
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]  # Сортировка по наименованию

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель товара"""

    name = models.CharField(max_length=200, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    image = models.ImageField(
        upload_to="products/",  # Папка для загрузки изображений
        verbose_name="Изображение",
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,  # При удалении категории удаляются все товары
        related_name="products",  # Для обратной связи category.products.all()
        verbose_name="Категория",
    )
    price = models.DecimalField(
        max_digits=10,  # Максимальное количество цифр
        decimal_places=2,  # Количество знаков после запятой
        verbose_name="Цена за покупку",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,  # Автоматически устанавливается при создании
        verbose_name="Дата создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,  # Автоматически обновляется при сохранении
        verbose_name="Дата последнего изменения",
    )
    is_published = models.BooleanField(default=True, verbose_name="статус публикации")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name"] # Сортировка по наименованию
        permissions  = [
            ('can_unpublish_product', 'Can unpublish product')
        ]



    def __str__(self):
        return self.name



