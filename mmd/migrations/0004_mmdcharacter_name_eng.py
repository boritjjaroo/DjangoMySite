# Generated by Django 3.2.4 on 2021-08-27 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mmd', '0003_mmdcharacter_mmdmaker_mmdmodel_mmdmovie_vocaloidsong'),
    ]

    operations = [
        migrations.AddField(
            model_name='mmdcharacter',
            name='name_eng',
            field=models.CharField(default='aaa', max_length=32),
            preserve_default=False,
        ),
    ]
