# Generated by Django 3.0.2 on 2020-03-04 12:47

from django.db import migrations, models
import myadmin.models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0063_experthelp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experthelp',
            name='ticket_code',
            field=models.CharField(default=myadmin.models.ExpertHelp.ticket_number, max_length=15, unique=True),
        ),
    ]
