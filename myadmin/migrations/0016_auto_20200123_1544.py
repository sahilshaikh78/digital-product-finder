# Generated by Django 3.0.2 on 2020-01-23 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0015_brand_profile_brand_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand_profile',
            name='brand_title',
            field=models.CharField(max_length=255),
        ),
    ]