# Generated by Django 2.0.1 on 2018-07-23 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fanyi', '0034_fyxmldiff_runningpid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fyxmldiff',
            name='create_time',
        ),
    ]