# Generated by Django 2.0.1 on 2018-04-29 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webqo', '0002_auto_20180428_1747'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='webqoqps',
            name='just_run_base',
        ),
        migrations.RemoveField(
            model_name='webqoqps',
            name='just_run_test',
        ),
    ]