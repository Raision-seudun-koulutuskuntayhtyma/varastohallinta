# Generated by Django 4.0.3 on 2023-01-21 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('varasto', '0063_alter_staff_audit_from_storage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff_audit',
            name='staff',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
