# Generated by Django 3.2.4 on 2021-11-05 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accbook', '0013_slipdata_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='is_balance',
            field=models.BooleanField(default=True),
        ),
    ]