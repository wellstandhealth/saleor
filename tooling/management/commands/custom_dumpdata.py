from django.core.management.commands import dumpdata
from tooling.constants import EXPORT_SALEOR_MODELS


class Command(dumpdata.Command):
    def handle(self, *app_labels, **options):
        return super().handle(*(app_labels + EXPORT_SALEOR_MODELS), **options)
