# Generated by Django 3.2.4 on 2021-11-05 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accbook', '0012_auto_20211105_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='slipdata',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]