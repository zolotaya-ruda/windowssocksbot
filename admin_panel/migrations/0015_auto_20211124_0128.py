# Generated by Django 3.2.5 on 2021-11-23 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0014_rename__type_task_type1'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='win_os',
            new_name='winos',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='x_oc',
            new_name='xoc',
        ),
    ]
