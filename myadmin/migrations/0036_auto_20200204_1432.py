# Generated by Django 3.0.2 on 2020-02-04 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0035_auto_20200204_1426'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product_type',
            old_name='product_types_id',
            new_name='product_type_id',
        ),
    ]
