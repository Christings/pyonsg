from django.db import models

# Create your models here.
class Business(models.Model):
	businame = models.CharField(max_length=64)


class Application(models.Model):
	appname = models.CharField(max_length=64)
	urlname = models.CharField(max_length=64)
	busi = models.ForeignKey(to='Business',to_field='id',on_delete=models.CASCADE)


class UserInfo(models.Model):
	user_name = models.CharField(max_length=64,unique=True)


class ReqInfo(models.Model):
	host_ip = models.CharField(max_length=128)
	trans_direct = models.CharField(max_length=20)
	isfromzh = models.CharField(max_length=10)
	req_text = models.CharField(max_length=2000)
	result = models.CharField(max_length=2000)
	user_fk = models.ForeignKey(to='UserInfo',to_field='user_name',on_delete=models.CASCADE)
	c_time = models.DateTimeField(auto_now=True)
	reqtype = models.CharField(max_length=20)


class UserToApp(models.Model):
	user_name = models.ForeignKey(to='UserInfo',to_field='user_name',on_delete=models.CASCADE)
	app_id = models.ForeignKey(to='Application', to_field='id',on_delete=models.CASCADE)



class FyMonitor(models.Model):
    create_time = models.CharField(max_length=50, default="")
    end_time = models.CharField(max_length=50, default="")
    user = models.CharField(max_length=50)
    status = models.IntegerField(default=0)
    monitorip = models.CharField(max_length=500, default="")
    monitoruser = models.CharField(max_length=500, default="")
    monitorpassw = models.CharField(max_length=500, default="")
    gpumem = models.TextField(default="")
    gpumemused = models.TextField(default="")
    h = models.ForeignKey(to="Host", to_field='id', on_delete=models.CASCADE)


class Host(models.Model):
    ip = models.GenericIPAddressField(db_index=True,unique=True)
    user = models.CharField(max_length=500, default="")
    passw = models.CharField(max_length=500, default="")




