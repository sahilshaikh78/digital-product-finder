# Generated by Django 3.0.2 on 2020-02-16 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0043_auto_20200216_1713'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product_feature',
            old_name='feature_value',
            new_name='product_feature_value',
        ),
        migrations.AddField(
            model_name='feature',
            name='feature_value',
            field=models.CharField(max_length=1, null=True),
        ),
    ]
