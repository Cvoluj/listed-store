# Generated by Django 5.0.6 on 2024-06-23 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]