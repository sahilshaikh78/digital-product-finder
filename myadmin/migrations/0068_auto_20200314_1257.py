# Generated by Django 3.0.2 on 2020-03-14 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0067_auto_20200310_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='brand_website',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='product_link',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
