from django.shortcuts import render
from fanyi import models


# Create your views here.


def qw_req(request):
	if request.method == 'GET':
		business_lst = models.Business.objects.all()
		app_lst = models.Application.objects.all()
		return render(request, 'qw_req.html', {'business_lst': business_lst,'app_lst': app_lst,'businame':'Webqw','app_name':"webqw请求调试"})


def qw_automation(request):
	if request.method == 'GET':
		business_lst = models.Business.objects.all()
		app_lst = models.Application.objects.all()
		return render(request, 'qw_automation.html', {'business_lst': business_lst,'app_lst': app_lst,'businame':'Webqw','app_name':"webqw性能对比自动化"})