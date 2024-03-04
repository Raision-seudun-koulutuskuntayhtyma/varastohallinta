# Generated by Django 4.0.3 on 2022-05-10 08:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('varasto', '0016_goods_amount_goods_units_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='ean',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='rental_event',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name=datetime.datetime(2022, 5, 10, 11, 0, 33, 7679)),
        ),
    ]