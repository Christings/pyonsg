from django.contrib import admin

# Register your models here.
from fanyi import models

admin.site.register(models.Business)
admin.site.register(models.Application)
admin.site.register(models.UserInfo)
admin.site.register(models.ReqInfo)
admin.site.register(models.UserToApp)