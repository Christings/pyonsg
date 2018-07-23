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
    status = models.IntegerField(default=0)
    runningPID = models.CharField(max_length=20, default="")

class FyDiff(models.Model):
    create_time = models.CharField(max_length=50, default="")
    start_time = models.CharField(max_length=50, default="")
    end_time = models.CharField(max_length=50, default="")
    user = models.CharField(max_length=50)
    status = models.IntegerField(default=0)
    hubcfgip = models.CharField(max_length=500, default="")
    hubcfguser = models.CharField(max_length=500, default="")
    hubcfgpassw = models.CharField(max_length=500, default="")
    hubcfgpath = models.CharField(max_length=500, default="")
    hubdatapath = models.CharField(max_length=500, default="")
    sercfgip = models.CharField(max_length=500, default="")
    sercfguser = models.CharField(max_length=500, default="")
    sercfgpassw = models.CharField(max_length=500, default="")
    sercfgpath = models.CharField(max_length=500, default="")
    serdatapath = models.CharField(max_length=500, default="")
    queryip = models.CharField(max_length=500, default="")
    queyruser = models.CharField(max_length=500, default="")
    querypassw = models.CharField(max_length=500, default="")
    querypath = models.CharField(max_length=500, default="")
    runningIP = models.CharField(max_length=50, default="")
    hubsvn = models.TextField(default="")
    sersvn = models.TextField(default="")
    errorlog = models.TextField(default="")
    testtag = models.CharField(max_length=500, default="")
    finished = models.IntegerField(default=0)
    diffnum = models.IntegerField(default=0)
    fromlan = models.CharField(max_length=20, default="")
    tolan = models.CharField(max_length=20, default="")
    isfromzh = models.CharField(max_length=10, default="")
    lan_sel = models.CharField(max_length=10, default="")


class DiffContent(models.Model):
    create_time = models.CharField(max_length=50, default="")
    user = models.CharField(max_length=50)
    diff_content = models.TextField(default="")
    diff_task = models.ForeignKey(to="FyDiff", to_field='id', on_delete=models.CASCADE)

class FyXmlDiff(models.Model):
    start_time = models.CharField(max_length=50, default="")
    end_time = models.CharField(max_length=50, default="")
    test_url = models.CharField(max_length=500, default="")
    base_url = models.CharField(max_length=500, default="")
    user = models.CharField(max_length=50)
    queryip = models.CharField(max_length=500, default="")
    queryuser = models.CharField(max_length=500, default="")
    querypassw = models.CharField(max_length=500, default="")
    querypath = models.CharField(max_length=500, default="")
    status = models.IntegerField(default=0)
    errorlog = models.TextField(default="")
    testtag = models.CharField(max_length=500, default="")
    finished = models.IntegerField(default=0)
    diffnum = models.IntegerField(default=0)
    runningPID = models.CharField(max_length=20, default="")


class XmlDiffContent(models.Model):
    create_time = models.CharField(max_length=50, default="")
    user = models.CharField(max_length=50)
    diff_content = models.TextField(default="")
    diff_task = models.ForeignKey(to="FyXmlDiff", to_field='id', on_delete=models.CASCADE)

