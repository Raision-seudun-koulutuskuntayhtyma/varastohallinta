# Generated by Django 4.0.3 on 2022-11-19 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('varasto', '0046_rental_event_contents_rental_event_units_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='units',
            name='unit',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
