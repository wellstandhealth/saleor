# Generated by Django 3.2.20 on 2023-09-27 06:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0186_remove_product_charge_taxes"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.RunSQL(
            """
            ALTER TABLE product_category
            ALTER COLUMN updated_at
            SET DEFAULT NOW();
            """,
            migrations.RunSQL.noop,
        ),
    ]