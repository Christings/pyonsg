# Generated by Django 2.0.1 on 2018-05-21 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fanyi', '0009_reqinfo_reqtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bbk_req_Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_ip', models.CharField(max_length=128)),
                ('trans_direct', models.CharField(max_length=20)),
                ('isfromzh', models.CharField(max_length=10)),
                ('req_text', models.CharField(max_length=2000)),
                ('result', models.CharField(max_length=2000)),
                ('c_time', models.DateTimeField(auto_now=True)),
                ('reqtype', models.CharField(max_length=20)),
                ('user_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fanyi.UserInfo', to_field='user_name')),
            ],
        ),
        migrations.CreateModel(
            name='fy_monitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.CharField(default='', max_length=50)),
                ('start_time', models.CharField(default='', max_length=50)),
                ('end_time', models.CharField(default='', max_length=50)),
                ('user', models.CharField(max_length=50)),
                ('status', models.IntegerField(default=0)),
                ('monitorip', models.CharField(default='', max_length=500)),
                ('monitoruser', models.CharField(default='', max_length=500)),
                ('monitorpassw', models.CharField(default='', max_length=500)),
                ('gpumem', models.TextField(default='')),
                ('gpumemused', models.TextField(default='')),
            ],
        ),
    ]