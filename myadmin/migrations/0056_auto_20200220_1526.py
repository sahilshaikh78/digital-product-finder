# Generated by Django 3.0.2 on 2020-02-20 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0055_auto_20200220_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_title',
            field=models.CharField(max_length=70),
        ),
    ]
