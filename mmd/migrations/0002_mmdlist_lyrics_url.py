# Generated by Django 3.2.4 on 2021-08-27 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mmd', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mmdlist',
            name='lyrics_url',
            field=models.CharField(max_length=512, null=True),
        ),
    ]
