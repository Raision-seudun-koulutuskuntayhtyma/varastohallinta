# Generated by Django 4.0.3 on 2022-11-25 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('varasto', '0055_rename_amount_x_units_goods_amount_x_contents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='cost_centre',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='goods',
            name='ean',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
    ]
