from django.db import models

# Create your models here.
class Business(models.Model):
	businame = models.CharField(max_length=64)





class Application(models.Model):
	appname = models.CharField(max_length=64)
	urlname = models.CharField(max_length=64)
	busi = models.ForeignKey(to='Business',to_field='id',on_delete=models.CASCADE)