# Generated by Django 5.1.7 on 2025-03-27 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='InBoundreadyProduct',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='OutBoundreadyProduct',
        ),
        migrations.AddField(
            model_name='inventory',
            name='Transaction_type',
            field=models.CharField(choices=[('Inbound', 'Inbound'), ('Outbound', 'Outbound')], default='Inbound', max_length=30),
        ),
    ]
