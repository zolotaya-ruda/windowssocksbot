# Generated by Django 3.2.5 on 2021-11-05 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0004_auto_20211104_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
