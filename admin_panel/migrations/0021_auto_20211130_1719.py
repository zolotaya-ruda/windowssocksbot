# Generated by Django 3.2.5 on 2021-11-30 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0020_auto_20211125_2249'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bot',
            old_name='is_winxp',
            new_name='is_server2012',
        ),
        migrations.AddField(
            model_name='bot',
            name='is_server2012r2',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bot',
            name='is_win81',
            field=models.BooleanField(default=False),
        ),
    ]
