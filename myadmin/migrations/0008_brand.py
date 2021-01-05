# Generated by Django 3.0.2 on 2020-01-22 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0007_auto_20200122_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('brand_id', models.AutoField(primary_key=True, serialize=False)),
                ('brand_name', models.CharField(max_length=255, unique=True)),
                ('brand_slug', models.SlugField(blank=True, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myadmin.Category')),
            ],
            options={
                'db_table': 'brand',
            },
        ),
    ]
