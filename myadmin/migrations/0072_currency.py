# Generated by Django 3.0.2 on 2020-03-14 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0071_auto_20200314_1758'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('currency_id', models.AutoField(primary_key=True, serialize=False)),
                ('currency_symbol', models.CharField(max_length=15)),
                ('currency_name', models.CharField(max_length=50)),
                ('country', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='currency', to='myadmin.Country')),
            ],
            options={
                'db_table': 'currency',
            },
        ),
    ]
