# Generated by Django 3.2.25 on 2024-05-02 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0007_auto_20231201_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='domain_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
    ]