# Generated by Django 3.0.2 on 2020-02-03 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0031_auto_20200203_1504'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product_type',
            old_name='type_description',
            new_name='product_type_description',
        ),
        migrations.RenameField(
            model_name='product_type',
            old_name='type_id',
            new_name='product_type_id',
        ),
        migrations.RenameField(
            model_name='product_type',
            old_name='type_name',
            new_name='product_type_name',
        ),
        migrations.RenameField(
            model_name='product_type',
            old_name='type_slug',
            new_name='product_type_slug',
        ),
    ]