# Generated by Django 3.0.2 on 2020-02-16 10:11

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0040_auto_20200207_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='brand_info',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
