# Generated by Django 4.2.23 on 2025-07-02 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_product_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
    ]
