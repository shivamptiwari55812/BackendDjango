# Generated by Django 5.1.7 on 2025-03-29 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_remove_inventory_productstatus_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='status',
            field=models.CharField(blank=True, choices=[('InStock', 'In Stock'), ('LowStock', 'Low Stock'), ('OutofStock', 'Out of Stock')], max_length=20),
        ),
    ]
