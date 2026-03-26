from django.core.management.base import BaseCommand
from django.core.management import call_command
from store.models import Category, Product
from django.utils import timezone
import os
import json


class Command(BaseCommand):
    help = "Добавляет тестовые продукты в базу данных"

    def add_arguments(self, parser):
        # Опциональный аргумент для использования фикстур
        parser.add_argument(
            "--use-fixtures",
            action="store_true",
            help="Использовать фикстуры для загрузки данных",
        )

        parser.add_argument(
            "--fixture-file",
            type=str,
            default="store/fixtures/test_products.json",
            help="Путь к файлу фикстуры (по умолчанию: store/fixtures/test_products.json)",
        )

    def handle(self, *args, **options):
        # Получаем опции
        use_fixtures = options["use_fixtures"]
        fixture_file = options["fixture_file"]

        # Шаг 1: Удаляем все существующие данные
        self.stdout.write(self.style.WARNING("Удаление существующих данных..."))
        self.clear_existing_data()

        # Шаг 2: Добавляем тестовые данные
        if use_fixtures and os.path.exists(fixture_file):
            self.stdout.write(
                self.style.WARNING(f"Загрузка данных из фикстуры: {fixture_file}")
            )
            self.load_from_fixture(fixture_file)
        else:
            self.stdout.write(
                self.style.WARNING("Создание тестовых данных через ORM...")
            )
            self.create_test_data()

        # Шаг 3: Выводим статистику
        self.show_statistics()

        self.stdout.write(self.style.SUCCESS("Тестовые продукты успешно добавлены!"))

    def clear_existing_data(self):
        """Удаление всех существующих данных"""
        # Удаляем все продукты
        products_count = Product.objects.count()
        Product.objects.all().delete()
        self.stdout.write(f"  - Удалено продуктов: {products_count}")

        # Удаляем все категории
        categories_count = Category.objects.count()
        Category.objects.all().delete()
        self.stdout.write(f"  - Удалено категорий: {categories_count}")

    def create_test_data(self):
        """Создание тестовых данных через ORM"""

        # Создаем категории
        categories_data = [
            {"name": "Смартфоны", "description": "Мобильные телефоны и смартфоны"},
            {"name": "Ноутбуки", "description": "Портативные компьютеры"},
            {"name": "Планшеты", "description": "Планшетные компьютеры"},
            {
                "name": "Аксессуары",
                "description": "Чехлы, защитные стекла и другие аксессуары",
            },
            {"name": "Наушники", "description": "Беспроводные и проводные наушники"},
        ]

        categories = []
        for cat_data in categories_data:
            category = Category.objects.create(**cat_data)
            categories.append(category)
            self.stdout.write(f"  + Создана категория: {category.name}")

        # Создаем продукты
        products_data = [
            {
                "name": "iPhone 15 Pro",
                "description": "Флагманский смартфон Apple с титановым корпусом",
                "price": 129990,
                "category": categories[0],  # Смартфоны
                "image": "products/iphone15.jpg",
            },
            {
                "name": "Samsung Galaxy S24 Ultra",
                "description": "Премиальный смартфон Samsung с S Pen",
                "price": 139990,
                "category": categories[0],  # Смартфоны
                "image": "products/samsung_s24.jpg",
            },
            {
                "name": "Xiaomi 14 Pro",
                "description": "Флагманский смартфон Xiaomi с камерой Leica",
                "price": 89990,
                "category": categories[0],  # Смартфоны
                "image": "products/xiaomi14.jpg",
            },
            {
                "name": "MacBook Pro 16",
                "description": "Профессиональный ноутбук Apple с чипом M3 Pro",
                "price": 249990,
                "category": categories[1],  # Ноутбуки
                "image": "products/macbook_pro.jpg",
            },
            {
                "name": "ASUS ROG Strix",
                "description": "Игровой ноутбук с RTX 4080",
                "price": 199990,
                "category": categories[1],  # Ноутбуки
                "image": "products/asus_rog.jpg",
            },
            {
                "name": "iPad Air",
                "description": "Легкий и мощный планшет Apple",
                "price": 59990,
                "category": categories[2],  # Планшеты
                "image": "products/ipad_air.jpg",
            },
            {
                "name": "Чехол для iPhone 15",
                "description": "Силиконовый чехол с MagSafe",
                "price": 3990,
                "category": categories[3],  # Аксессуары
                "image": "products/iphone_case.jpg",
            },
            {
                "name": "AirPods Pro",
                "description": "Беспроводные наушники с активным шумоподавлением",
                "price": 24990,
                "category": categories[4],  # Наушники
                "image": "products/airpods_pro.jpg",
            },
            {
                "name": "Sony WH-1000XM5",
                "description": "Премиальные наушники с шумоподавлением",
                "price": 34990,
                "category": categories[4],  # Наушники
                "image": "products/sony_xm5.jpg",
            },
        ]

        for prod_data in products_data:
            product = Product.objects.create(**prod_data)
            self.stdout.write(f"  + Создан продукт: {product.name} ({product.price} ₽)")

    def load_from_fixture(self, fixture_file):
        """Загрузка данных из фикстуры"""
        try:
            call_command("loaddata", fixture_file)
            self.stdout.write(
                self.style.SUCCESS(f"  Данные загружены из {fixture_file}")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  Ошибка загрузки фикстуры: {e}"))
            self.stdout.write(
                self.style.WARNING("  Создаю тестовые данные через ORM...")
            )
            self.create_test_data()

    def show_statistics(self):
        """Вывод статистики по созданным данным"""
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS("СТАТИСТИКА:"))

        categories_count = Category.objects.count()
        products_count = Product.objects.count()

        self.stdout.write(f"Всего категорий: {categories_count}")
        self.stdout.write(f"Всего продуктов: {products_count}")

        if categories_count > 0:
            self.stdout.write("\nКатегории:")
            for category in Category.objects.all():
                prod_in_cat = Product.objects.filter(category=category).count()
                self.stdout.write(f"  - {category.name}: {prod_in_cat} продуктов")

        if products_count > 0:
            self.stdout.write("\nПримеры продуктов:")
            for product in Product.objects.all()[:5]:  # Первые 5 продуктов
                self.stdout.write(
                    f"  - {product.name}: {product.price} ₽ ({product.category.name})"
                )
