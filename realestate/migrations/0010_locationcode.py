# Generated by Django 3.2.4 on 2021-09-03 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0009_alter_mylanditem_is_multi_family'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=16)),
            ],
        ),
    ]
