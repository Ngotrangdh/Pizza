# Generated by Django 2.0.3 on 2020-05-31 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20200531_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariant',
            name='size',
            field=models.CharField(choices=[('small', 'Small'), ('large', 'Large'), ('one size', 'One Size')], default='one size', max_length=8),
        ),
    ]