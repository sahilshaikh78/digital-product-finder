# Generated by Django 3.0.2 on 2020-01-23 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0013_auto_20200123_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='country_name',
            field=models.CharField(max_length=255),
        ),
    ]
