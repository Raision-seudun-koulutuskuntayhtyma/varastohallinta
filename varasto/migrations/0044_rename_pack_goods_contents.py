# Generated by Django 4.0.3 on 2022-11-18 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('varasto', '0043_alter_goods_pack'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goods',
            old_name='pack',
            new_name='contents',
        ),
    ]
