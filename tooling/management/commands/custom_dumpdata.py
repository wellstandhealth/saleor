import os
from dotenv import load_dotenv
from django.core.management.commands import dumpdata

load_dotenv()
_MODELS = tuple(os.getenv("SALEOR_NATURAL_KEY_MODELS").split(","))


class Command(dumpdata.Command):
    def handle(self, *app_labels, **options):
        return super().handle(*_MODELS, **options)
