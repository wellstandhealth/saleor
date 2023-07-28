from django.db import models
from saleor.product.models import Product, ProductManager, ProductsQueryset


class CustomProductManager(ProductManager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


# class CustomProductsQueryset(ProductsQueryset):
#     def get_by_natural_key(self, slug):
#         return self.get(slug=slug)
#
#
# ProductManager = models.Manager.from_queryset(CustomProductsQueryset)
Product.objects = CustomProductManager()


def natural_key(self):
    return (self.slug,)


Product.natural_key = natural_key
