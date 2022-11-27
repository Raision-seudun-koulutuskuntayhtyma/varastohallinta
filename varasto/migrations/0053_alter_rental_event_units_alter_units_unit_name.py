# Generated by Django 4.0.3 on 2022-11-24 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('varasto', '0052_alter_goods_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental_event',
            name='units',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='varasto.units'),
        ),
        migrations.AlterField(
            model_name='units',
            name='unit_name',
            field=models.CharField(blank=True, max_length=25, null=True, unique=True),
        ),
    ]
