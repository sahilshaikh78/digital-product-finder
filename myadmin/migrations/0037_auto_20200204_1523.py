# Generated by Django 3.0.2 on 2020-02-04 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0036_auto_20200204_1432'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_starting_price',
            new_name='product_price',
        ),
    ]
