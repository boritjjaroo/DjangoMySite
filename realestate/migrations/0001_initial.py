# Generated by Django 3.2.4 on 2021-06-27 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ListItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_id', models.IntegerField()),
                ('price', models.IntegerField()),
                ('address', models.CharField(max_length=128)),
            ],
        ),
    ]
