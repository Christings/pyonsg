from django.shortcuts import render
from fanyi import models
from fanyi import requestData

# Create your views here.


def qo_req(request):
	if request.method == 'GET':
		business_lst = models.Business.objects.all()
		app_lst = models.Application.objects.all()
		req_lst = models.ReqInfo.objects.all()
		timea =models.ReqInfo.objects.all().values()
		# for item in timea:
		# 	print(item)
		return render(request, 'qo_req.html', {'business_lst': business_lst,'app_lst': app_lst,'businame':'Webqo','app_name':"webqo性能对比自动化"})


def qo_automation(request):
	if request.method == 'GET':
		business_lst = models.Business.objects.all()
		app_lst = models.Application.objects.all()
		req_lst = models.ReqInfo.objects.all()
		timea =models.ReqInfo.objects.all().values()
		# for item in timea:
		# 	print(item)
		return render(request, 'qo_automation.html', {'business_lst': business_lst,'app_lst': app_lst,'businame':'Webqo','app_name':"webqo性能对比自动化"})