# Generated by Django 2.0.6 on 2018-08-01 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webqw', '0007_auto_20180731_1450'),
    ]

    operations = [
        migrations.CreateModel(
            name='webqwlongdiff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.CharField(default='', max_length=50)),
                ('start_time', models.CharField(default='', max_length=50)),
                ('end_time', models.CharField(default='', max_length=50)),
                ('user', models.CharField(max_length=50)),
                ('status', models.IntegerField(default=0)),
                ('step', models.IntegerField(default=-1)),
                ('testitem', models.IntegerField(default=0)),
                ('newdataip', models.CharField(default='', max_length=500)),
                ('newdatauser', models.CharField(default='', max_length=500)),
                ('newdatapassw', models.CharField(default='', max_length=500)),
                ('newdatapath', models.CharField(default='', max_length=500)),
                ('newdata_topath', models.CharField(default='', max_length=500)),
                ('newconfip', models.CharField(default='', max_length=500)),
                ('newconfuser', models.CharField(default='', max_length=500)),
                ('newconfpassw', models.CharField(default='', max_length=500)),
                ('newconfpath', models.CharField(default='', max_length=500)),
                ('runningIP', models.CharField(default='', max_length=50)),
                ('testsvn', models.TextField(default='')),
                ('basesvn', models.TextField(default='')),
                ('errorlog', models.TextField(default='')),
                ('cost_test', models.TextField(default='')),
                ('cost_base', models.TextField(default='')),
                ('query_ip', models.CharField(default='', max_length=500)),
                ('query_user', models.CharField(default='', max_length=50)),
                ('query_pwd', models.CharField(default='', max_length=50)),
                ('query_path', models.CharField(default='', max_length=500)),
                ('testtag', models.CharField(default='', max_length=500)),
            ],
        ),
        migrations.RemoveField(
            model_name='webqwqps',
            name='query_ip',
        ),
        migrations.RemoveField(
            model_name='webqwqps',
            name='query_path',
        ),
        migrations.RemoveField(
            model_name='webqwqps',
            name='query_pwd',
        ),
        migrations.RemoveField(
            model_name='webqwqps',
            name='query_user',
        ),
        migrations.AlterField(
            model_name='webqwqps',
            name='press_expid',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='webqwqps',
            name='press_qps',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='webqwqps',
            name='press_rate',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='webqwqps',
            name='press_time',
            field=models.IntegerField(),
        ),
    ]
