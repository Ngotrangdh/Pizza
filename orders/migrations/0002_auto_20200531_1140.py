# Generated by Django 2.0.3 on 2020-05-31 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductVariants',
            new_name='ProductVariant',
        ),
    ]
