# Generated by Django 5.1.7 on 2025-03-28 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_remove_inventory_inboundreadyproduct_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='Warehouse',
        ),
    ]
