# Generated by Django 3.2.4 on 2021-12-06 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accbook', '0019_auto_20211205_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='fnprod',
            name='account',
            field=models.ForeignKey(default=100, on_delete=django.db.models.deletion.CASCADE, to='accbook.accounts'),
            preserve_default=False,
        ),
    ]