# Generated by Django 2.0.3 on 2020-06-05 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='orders.OrderItem'),
        ),
    ]
