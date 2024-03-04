# Generated by Django 4.0.3 on 2022-05-10 09:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('varasto', '0018_alter_goods_ean_alter_rental_event_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='amount',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='goods',
            name='ean',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='goods',
            name='units',
            field=models.CharField(blank=True, choices=[('unit', 'kpl'), ('litre', 'l')], default='unit', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='rental_event',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name=datetime.datetime(2022, 5, 10, 12, 3, 37, 794236)),
        ),
    ]