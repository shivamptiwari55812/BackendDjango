# Generated by Django 5.1.7 on 2025-03-31 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outbound', '0002_receiverside_modeoftransport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receiverside',
            name='ModeOfTransport',
            field=models.CharField(blank=True, default='By Road', max_length=100, null=True),
        ),
    ]
