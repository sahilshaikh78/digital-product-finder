# Generated by Django 3.0.2 on 2020-02-04 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0037_auto_20200204_1523'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feature',
            name='feature_description',
        ),
    ]
