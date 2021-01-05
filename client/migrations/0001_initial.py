# Generated by Django 3.0.2 on 2020-01-06 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('contact_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=255)),
                ('mobile', models.CharField(max_length=10)),
                ('message', models.CharField(max_length=5000)),
            ],
            options={
                'db_table': 'contact',
            },
        ),
    ]
