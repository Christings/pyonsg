# Generated by Django 2.0.1 on 2018-07-09 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fanyi', '0020_auto_20180709_1422'),
    ]

    operations = [
        migrations.RenameField(
            model_name='diffcontent',
            old_name='diffcontent',
            new_name='content',
        ),
    ]