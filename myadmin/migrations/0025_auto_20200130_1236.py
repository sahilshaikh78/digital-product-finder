# Generated by Django 3.0.2 on 2020-01-30 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0024_auto_20200125_1750'),
    ]

    operations = [
        migrations.RenameField(
            model_name='brand_profile',
            old_name='brand',
            new_name='brand_id',
        ),
        migrations.RenameField(
            model_name='brand_profile',
            old_name='brand_category',
            new_name='category_id',
        ),
        migrations.RenameField(
            model_name='brand_profile',
            old_name='brand_country',
            new_name='country_id',
        ),
    ]
