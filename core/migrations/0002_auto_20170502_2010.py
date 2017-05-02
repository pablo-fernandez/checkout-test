# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_products(apps, schema_editor):
    Product = apps.get_model('core', 'Product')
    Product.objects.create(name='Guitarra Criolla', price='1500.00')
    Product.objects.create(name='Guitarra Electrica', price='5000.00')
    Product.objects.create(name='Piano', price='8000.00')
    Product.objects.create(name='Microfono', price='2500.00')


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_products, reverse_code=migrations.RunPython.noop),
    ]
