# Generated by Django 3.2.4 on 2021-07-01 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0007_auto_20210630_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='mylanditem',
            name='is_multi_family',
            field=models.NullBooleanField(),
        ),
    ]
