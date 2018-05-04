from django.shortcuts import render,HttpResponse,redirect
from django.forms.models import model_to_dict
from webqw import models
from fanyi import models as layout
import time,json


# Create your views here.


def qw_req(request):
	if request.method == 'GET':
		business_lst = models.Business.objects.all()
		app_lst = models.Application.objects.all()
		return render(request, 'qw_req.html', {'business_lst': business_lst,'app_lst': app_lst,'businame':'Webqw','app_name':"webqw请求调试"})


def qw_task_cancel(request):
	# login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	# try:
	# 	user_id = request.COOKIES['uid']
	# except:
	# 	return redirect(login_url)
	ret = {'status': True, 'errro': None, 'data': None}
	try:
		re_add_task_d = request.POST.get('task_id')
		models.webqwqps.objects.filter(id=re_add_task_d).update(status=6)
	except Exception as e:
		ret['error'] = 'error:' + str(e)
		ret['status'] = False
	return HttpResponse(json.dumps(ret))

def qw_task_readd(request):
	# login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	# try:
	# 	user_id = request.COOKIES['uid']
	# except:
	# 	return redirect(login_url)
	ret = {'status': True, 'errro': None, 'data': None}
	re_add_task_d = request.POST.get('task_id')
	try:
		task_detail = models.webqwqps.objects.get(id=re_add_task_d)
		task_detail_todic = model_to_dict(task_detail)
		task_detail_todic.pop('id')
		task_detail_todic['create_time'] = get_now_time()
		task_detail_todic['start_time'] =""
		task_detail_todic['end_time'] =""
		task_detail_todic['testitem'] = 1
		task_detail_todic['status'] = 0
		task_detail_todic['errorlog'] = ""
		task_detail_todic['cost_test'] = ""
		task_detail_todic['cost_base'] = ""
		task_detail_todic['runningIP'] = ""
		models.webqwqps.objects.create(**task_detail_todic)
	except Exception as e:
		print(e)
		ret['error'] = 'error:'+str(e)
		ret['status'] = False
	return HttpResponse(json.dumps(ret))


def qw_task_detail(request,task_id):
	# login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	# try:
	# 	user_id = request.COOKIES['uid']
	# except:
	# 	return redirect(login_url)
	task_detail = models.webqwqps.objects.filter(id=task_id)
	business_lst = layout.Business.objects.all()
	app_lst = layout.Application.objects.all()
	return render(request, 'qw_task_tail.html',{'business_lst': business_lst, 'app_lst': app_lst, 'businame': 'Webqw', 'app_name': "webqw性能对比自动化",'topic':'任务详情','task_detail': task_detail})

def qw_automation(request):
	# login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	# try:
	# 	user_id = request.COOKIES['uid']
	# except:
	# 	return redirect(login_url)
	if request.method == 'GET':
		task_list = models.webqwqps.objects.order_by('id')[::-1]
		business_lst = layout.Business.objects.all()
		app_lst = layout.Application.objects.all()
		return render(request, 'qw_automation.html',{'business_lst': business_lst,'app_lst': app_lst,'businame':'Webqw','app_name':"webqw性能对比自动化",'task_list': task_list})
	elif request.method== 'POST':
		ret = {'status': True, 'errro': None, 'data': None}
		test_svn = str_dos2unix(request.POST.get('qw_testsvn'))
		base_svn = str_dos2unix(request.POST.get('qw_basesvn'))
		newconfip = str_dos2unix(request.POST.get('new_conf_ip'))
		newconfuser = str_dos2unix(request.POST.get('new_conf_user'))
		newconfpassw = str_dos2unix(request.POST.get('new_conf_pass'))
		newconfpath = str_dos2unix(request.POST.get('new_conf_path'))
		newdataip = str_dos2unix(request.POST.get('new_data_ip'))
		newdatauser = str_dos2unix(request.POST.get('new_data_user'))
		newdatapassw = str_dos2unix(request.POST.get('new_data_pass'))
		newdatapath = str_dos2unix(request.POST.get('new_data_path'))
		press_qps = str_dos2unix(request.POST.get('qw_qps'))
		press_time = str_dos2unix(request.POST.get('qw_press_time'))
		if press_qps=="":
			press_qps=1000
		if press_time=="":
			press_time=15
		print('test_svn:'+test_svn,'base_svn:'+base_svn,'newconfip:'+newconfip,'newconfuser:'+newconfuser,'newconfpassw:'+newconfpassw,'newconfpath:'+newconfpath,'newdataip:'+newdataip,'newdatauser:'+newdatauser,'newdatapassw:'+newdatapassw,'newdatapath:'+newdatapath)
		try:
			models.webqwqps.objects.create(create_time=get_now_time(), user='zhangjingjun', testitem=1, testsvn=test_svn, basesvn=base_svn,
								newconfip=newconfip, newconfuser=newconfuser, newconfpassw=newconfpassw,
								newconfpath=newconfpath, newdataip=newdataip, newdatauser=newdatauser,
								newdatapassw=newdatapassw, newdatapath=newdatapath,press_qps=press_qps, press_time=press_time)
		except Exception as e:
			ret['error'] = 'error:'+str(e)
			ret['status'] = False
		return HttpResponse(json.dumps(ret))
	else:
		return HttpResponse('requestError')


def get_now_time():
    timeArray = time.localtime()
    return  time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


def str_dos2unix(input):
    return input.replace('\r\n', '\n').replace(' ', '')