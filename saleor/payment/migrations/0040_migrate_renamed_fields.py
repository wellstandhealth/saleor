from django.apps import apps as registry
from django.db import migrations
from django.db.models.signals import post_migrate

from .tasks.saleor3_12 import (
    transaction_event_migrate_name_to_message,
    transaction_event_migrate_reference_to_psp_reference,
    transaction_item_migrate_reference_to_psp_reference,
    transaction_item_migrate_type_to_name,
    transaction_item_migrate_voided_to_canceled,
    transaction_event_migrate_name_to_message_task,
    transaction_event_migrate_reference_to_psp_reference_task,
    transaction_item_migrate_reference_to_psp_reference_task,
    transaction_item_migrate_type_to_name_task,
    transaction_item_migrate_voided_to_canceled_task,
)
from ... import __version__


def migrate_data_for_renamed_fields(apps, _schema_editor):
    def on_migrations_complete(sender=None, **kwargs):
        transaction_event_migrate_name_to_message_task.delay()
        transaction_event_migrate_reference_to_psp_reference_task.delay()
        transaction_item_migrate_reference_to_psp_reference_task.delay()
        transaction_item_migrate_type_to_name_task.delay()
        transaction_item_migrate_voided_to_canceled_task.delay()

    if __version__.startswith("3.12"):
        sender = registry.get_app_config("payment")
        post_migrate.connect(on_migrations_complete, weak=False, sender=sender)
    else:
        TransactionItem = apps.get_model("payment", "TransactionItem")
        TransactionEvent = apps.get_model("payment", "TransactionEvent")
        transaction_event_migrate_name_to_message(TransactionEvent)
        transaction_event_migrate_reference_to_psp_reference(TransactionEvent)
        transaction_item_migrate_reference_to_psp_reference(TransactionItem)
        transaction_item_migrate_type_to_name(TransactionItem)
        transaction_item_migrate_voided_to_canceled(TransactionItem)


class Migration(migrations.Migration):
    dependencies = [
        ("payment", "0039_transactionevent_currency"),
    ]

    operations = [
        migrations.RunPython(migrate_data_for_renamed_fields, migrations.RunPython.noop)
    ]