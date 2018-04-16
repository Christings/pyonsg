from django.shortcuts import render,HttpResponse,redirect
from django.forms.models import model_to_dict
from webqo import models
from fanyi import models as layout
import math,time,json


# Create your views here.


def qo_req(request):
	if request.method == 'GET':
		business_lst = layout.Business.objects.all()
		app_lst = layout.Application.objects.all()
		req_lst = layout.ReqInfo.objects.all()
		timea =layout.ReqInfo.objects.all().values()
		# for item in timea:
		# 	print(item)
		return render(request, 'qo_req.html', {'business_lst': business_lst,'app_lst': app_lst,'businame':'Webqo','app_name':"webqo请求调试"})


def qo_task_cancel(request):
	# login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	# try:
	# 	user_id = request.COOKIES['uid']
	# except:
	# 	return redirect(login_url)
	ret = {'status': True, 'errro': None, 'data': None}
	try:
		re_add_task_d = request.POST.get('task_id')
		models.webqoqps.objects.filter(id=re_add_task_d).update(status=6)
	except Exception as e:
		ret['error'] = 'error:' + str(e)
		ret['status'] = False
	return HttpResponse(json.dumps(ret))

def qo_task_readd(request):
	# login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	# try:
	# 	user_id = request.COOKIES['uid']
	# except:
	# 	return redirect(login_url)
	ret = {'status': True, 'errro': None, 'data': None}
	re_add_task_d = request.POST.get('task_id')
	try:
		task_detail = models.webqoqps.objects.get(id=re_add_task_d)
		task_detail_todic = model_to_dict(task_detail)
		task_detail_todic.pop('id')
		task_detail_todic['create_time'] = get_now_time()
		task_detail_todic['start_time'] =""
		task_detail_todic['end_time'] =""
		task_detail_todic['testitem'] = 1
		models.webqoqps.objects.create(**task_detail_todic)
	except Exception as e:
		print(e)
		ret['error'] = 'error:'+str(e)
		ret['status'] = False
	return HttpResponse(json.dumps(ret))


def qo_task_detail(request,task_id):
	# login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	# try:
	# 	user_id = request.COOKIES['uid']
	# except:
	# 	return redirect(login_url)
	task_detail = models.webqoqps.objects.filter(id=task_id)
	business_lst = layout.Business.objects.all()
	app_lst = layout.Application.objects.all()
	return render(request, 'qo_task_tail.html',{'business_lst': business_lst, 'app_lst': app_lst, 'businame': 'Webqo', 'app_name': "webqo性能对比自动化",'topic':'任务详情','task_detail': task_detail})

def qo_automation(request):
	# login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	# try:
	# 	user_id = request.COOKIES['uid']
	# except:
	# 	return redirect(login_url)
	if request.method == 'GET':
		task_list = models.webqoqps.objects.order_by('id')[::-1]
		business_lst = layout.Business.objects.all()
		app_lst = layout.Application.objects.all()
		return render(request, 'qo_automation.html',{'business_lst': business_lst,'app_lst': app_lst,'businame':'Webqo','app_name':"webqo性能对比自动化",'task_list': task_list})
	elif request.method== 'POST':
		ret = {'status': True, 'errro': None, 'data': None}
		test_svn = str_dos2unix(request.POST.get('qo_testsvn'))
		base_svn = str_dos2unix(request.POST.get('qo_basesvn'))
		newconfip = str_dos2unix(request.POST.get('new_conf_ip'))
		newconfuser = str_dos2unix(request.POST.get('new_conf_user'))
		newconfpassw = str_dos2unix(request.POST.get('new_conf_pass'))
		newconfpath = str_dos2unix(request.POST.get('new_conf_path'))
		newdataip = str_dos2unix(request.POST.get('new_data_ip'))
		newdatauser = str_dos2unix(request.POST.get('new_data_user'))
		newdatapassw = str_dos2unix(request.POST.get('new_data_pass'))
		newdatapath = str_dos2unix(request.POST.get('new_data_path'))
		press_qps = str_dos2unix(request.POST.get('qo_qps'))
		press_time = str_dos2unix(request.POST.get('qo_press_time'))
		if test_svn=="":
			just_run_base = 1
			just_run_test = 0
		elif base_svn=="":
			just_run_base = 0
			just_run_test = 1
		else:
			just_run_base = 1
			just_run_test = 1
		if press_qps=="":
			press_qps=1000
		if press_time=="":
			press_time=15
		print('test_svn:'+test_svn,'base_svn:'+base_svn,'newconfip:'+newconfip,'newconfuser:'+newconfuser,'newconfpassw:'+newconfpassw,'newconfpath:'+newconfpath,'newdataip:'+newdataip,'newdatauser:'+newdatauser,'newdatapassw:'+newdatapassw,'newdatapath:'+newdatapath)
		try:
			models.webqoqps.objects.create(create_time=get_now_time(), user='zhangjingjun', testitem=1, testsvn=test_svn, basesvn=base_svn,
								newconfip=newconfip, newconfuser=newconfuser, newconfpassw=newconfpassw,
								newconfpath=newconfpath, newdataip=newdataip, newdatauser=newdatauser,
								newdatapassw=newdatapassw, newdatapath=newdatapath, just_run_test=just_run_test,
								just_run_base=just_run_base, press_qps=press_qps, press_time=press_time)
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


