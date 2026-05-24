from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType

from store.models import Product


class Command(BaseCommand):
    help = 'Create or update the "Модератор продуктов" group with product moderation permissions.'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Модератор продуктов")
        product_content_type = ContentType.objects.get_for_model(Product)
        permissions = Permission.objects.filter(
            content_type=product_content_type,
            codename__in=["can_unpublish_product", "delete_product"],
        )
        group.permissions.set(permissions)

        action = "created" if created else "updated"
        self.stdout.write(
            self.style.SUCCESS(
                f'Group "Модератор продуктов" {action} with product moderation permissions.'
            )
        )
