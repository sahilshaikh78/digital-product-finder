# Generated by Django 3.0.2 on 2020-02-16 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0044_auto_20200216_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='feature_value',
            field=models.CharField(max_length=1),
        ),
    ]
