from django.apps import AppConfig


def get_by_natural_key(self, slug):
    return self.get(slug=slug)


def natural_key(self):
    return (self.slug,)


class ToolingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tooling'

    def ready(self):
        from saleor.product.models import Product, ProductManager

        ProductManager.get_by_natural_key = get_by_natural_key
        Product.objects = ProductManager()
        Product.natural_key = natural_key
