# Generated by Django 3.2.4 on 2021-11-01 06:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accbook', '0006_auto_20211031_1924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditcard',
            name='interest_rate',
        ),
    ]