# Generated by Django 3.0.2 on 2020-01-24 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0019_auto_20200123_1904'),
    ]

    operations = [
        migrations.RenameField(
            model_name='brand_profile',
            old_name='brand_id',
            new_name='brand',
        ),
    ]
