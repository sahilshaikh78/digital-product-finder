# Generated by Django 3.0.2 on 2020-02-16 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0045_auto_20200216_1728'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feature',
            old_name='feature_value',
            new_name='feature_has_value',
        ),
        migrations.RemoveField(
            model_name='feature',
            name='feature_category_type',
        ),
        migrations.AddField(
            model_name='feature',
            name='feature_product_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myadmin.Product_type'),
        ),
    ]
