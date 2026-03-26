from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    ordering = ("id",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price", "category"]
    list_display_links = ["id", "name"]
    list_filter = ["category"]
    search_fields = ["name", "description"]
    ordering = ["-id"]
    list_editable = ["price"]
    list_per_page = 50
    readonly_fields = ["created_at", "updated_at"]  # Даты только для чтения
