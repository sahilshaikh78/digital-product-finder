# Generated by Django 3.0.2 on 2020-01-23 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0016_auto_20200123_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand_profile',
            name='brand_status',
            field=models.CharField(default='draft', max_length=100),
        ),
    ]
