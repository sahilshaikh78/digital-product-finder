# Generated by Django 3.0.2 on 2020-06-28 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0075_auto_20200628_1509'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experthelp',
            name='category',
        ),
        migrations.AddField(
            model_name='experthelp',
            name='customer_help_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categories', to='myadmin.Category'),
        ),
    ]
