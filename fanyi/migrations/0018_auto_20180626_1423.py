# Generated by Django 2.0.1 on 2018-06-26 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fanyi', '0017_fydiff'),
    ]

    operations = [
        migrations.AddField(
            model_name='fydiff',
            name='queryip',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='fydiff',
            name='querypassw',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='fydiff',
            name='querypath',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='fydiff',
            name='queyruser',
            field=models.CharField(default='', max_length=500),
        ),
    ]