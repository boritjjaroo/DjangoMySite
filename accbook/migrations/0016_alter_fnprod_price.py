# Generated by Django 3.2.4 on 2021-12-05 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accbook', '0015_fnprod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fnprod',
            name='price',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
    ]