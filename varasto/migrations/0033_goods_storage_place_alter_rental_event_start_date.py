# Generated by Django 4.0.3 on 2022-09-13 07:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('varasto', '0032_rename_storge_customuser_storage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='storage_place',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='rental_event',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name=datetime.datetime(2022, 9, 13, 10, 36, 0, 201264)),
        ),
    ]
