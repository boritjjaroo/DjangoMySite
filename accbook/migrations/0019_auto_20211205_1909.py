# Generated by Django 3.2.4 on 2021-12-05 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accbook', '0018_fntrade'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fntrade',
            old_name='date',
            new_name='buy_date',
        ),
        migrations.AddField(
            model_name='fntrade',
            name='sell_date',
            field=models.DateTimeField(null=True),
        ),
    ]
