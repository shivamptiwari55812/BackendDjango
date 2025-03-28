# Generated by Django 5.1.7 on 2025-03-27 18:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('outbound', '0001_initial'),
        ('registration', '0001_initial'),
        ('transport', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceBill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Invoice_number', models.CharField(max_length=100)),
                ('Bill_date', models.DateField(auto_now_add=True)),
                ('Bill_number', models.IntegerField(blank=True, null=True)),
                ('Bill_time', models.DateTimeField(auto_now=True)),
                ('Bill_validity', models.DateField()),
                ('ValueOfGoods', models.IntegerField(default=0)),
                ('ReasonForTransport', models.TextField()),
                ('CEWBno', models.IntegerField()),
                ('MultiVehInfo', models.IntegerField()),
                ('Bill_pdf', models.FileField(default='default_bill.pdf', upload_to='bills/')),
                ('Driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transport.driver')),
                ('Receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='outbound.receiverside')),
                ('Transporter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transport.transporter')),
                ('Warehouse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='registration.warehouse')),
            ],
        ),
    ]
