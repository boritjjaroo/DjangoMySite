# Generated by Django 3.2.4 on 2021-10-29 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accbook', '0003_auto_20211029_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='deposit',
            name='number',
            field=models.CharField(default='', max_length=32),
        ),
    ]
