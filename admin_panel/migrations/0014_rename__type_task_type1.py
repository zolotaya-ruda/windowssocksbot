# Generated by Django 3.2.5 on 2021-11-23 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0013_auto_20211124_0102'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='_type',
            new_name='type1',
        ),
    ]
