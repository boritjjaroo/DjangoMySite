# Generated by Django 3.2.4 on 2021-11-03 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accbook', '0009_auto_20211102_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='slip',
            name='is_temporary',
            field=models.BooleanField(default=False),
        ),
    ]
