import base64
from saleor.attribute.models import AssignedProductAttributeValue
from saleor.celeryconf import app
from saleor.channel.models import Channel

from saleor.product.models import (
    Product,
    ProductChannelListing,
    ProductMedia,
    CollectionProduct,
)
from algoliasearch.search.client import SearchClientSync

from saleor.product.product_images import get_product_image_thumbnail_url
from saleor.thumbnail.models import Thumbnail


class ProcessingException(Exception):
    def __init__(self, message):
        self.message = message

        super().__init__(self.message)


@app.task(
    autoretry_for=(Exception, ProcessingException),
    retry_backoff=5,
    retry_kwargs={"max_retries": 1},
)
def index_products():
    # get these from Secret Manager
    app_id = "DEY3XXKZHX"
    app_key = "e1affb4c79aea22b38e44da7b3e06a9d"
    index_name = "wellstand_storefront_qa"

    client = SearchClientSync(app_id, app_key)

    products = Product.objects.all()
    for product in products:
        # Create the base record to be indexed
        external_id = base64.b64encode(f"Product:{product.id}".encode("UTF-8")).decode(
            "UTF-8"
        )

        record = {
            "id": external_id,
            "name": product.name,
            "attributes": {},
            "description": product.description,
            "descriptionPlainText": product.description_plaintext,
            "slug": product.slug,
            "thumbnail": None,
            "productType": product.product_type.name,
            "category": product.category.name,
            "collections": [],
            "channels": [],
            "metadata": {},
            "objectID": external_id,
        }

        # Add attributes
        product_attribute_values = AssignedProductAttributeValue.objects.filter(
            product=product
        )
        for attribute in product_attribute_values:
            nv_pair = attribute.value.name.split(":")
            record["attributes"][nv_pair[0]] = nv_pair[1]

        # Add channels
        product_channels = product.channel_listings.all()
        for product_channel in product_channels:
            channel = product_channel.channel
            record["channels"].append(channel.slug)

        product_collections = CollectionProduct.objects.filter(product=product)
        for collection_product in product_collections:
            record["collections"].append(collection_product.collection.name)

        # Add thumbnail
        product_media = ProductMedia.objects.filter(product=product).first()
        thumbnail_url = get_product_image_thumbnail_url(product_media, 1024)

        # this is hardcoded...should try to use storage configuration
        if thumbnail_url is not None:
            thumbnail_url = thumbnail_url.replace(
                "/media/",
                "https://storage.googleapis.com/pharmacy-io-qa-media/us-central1/",
            )
            record["thumbnail"] = thumbnail_url
        # Add record to an index
        save_response = client.save_object(index_name=index_name, body=record)

        # Wait until indexing is done
        client.wait_for_task(index_name=index_name, task_id=save_response.task_id)
