# Generated by Django 5.0.6 on 2024-06-24 14:04

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_cart', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='created_at',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='updated_at',
            new_name='updated',
        ),
        migrations.RenameField(
            model_name='cartitem',
            old_name='created_at',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='cartitem',
            old_name='updated_at',
            new_name='updated',
        ),
        migrations.AddField(
            model_name='cart',
            name='public_id',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='public_id',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
