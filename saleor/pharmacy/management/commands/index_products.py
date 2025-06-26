import logging
from django.core.management.base import BaseCommand, CommandError
from saleor.pharmacy.tasks import index_products

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Index all products into the search engine."

    def handle(self, *args, **options):
        try:
            index_products()
            self.stdout.write(self.style.SUCCESS("Successfully indexed all products."))
        except Exception as e:
            logger.error(f"Error indexing products: {e}")
            raise CommandError("Failed to index products.")
