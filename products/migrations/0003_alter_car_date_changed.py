# Generated by Django 4.0.1 on 2022-01-20 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_car_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='date_changed',
            field=models.TimeField(auto_now=True, null=True),
        ),
    ]
