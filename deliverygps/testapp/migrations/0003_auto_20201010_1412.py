# Generated by Django 3.0.8 on 2020-10-10 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0002_auto_20201010_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_lat',
            field=models.DecimalField(decimal_places=7, max_digits=9),
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_lon',
            field=models.DecimalField(decimal_places=7, max_digits=9),
        ),
    ]
