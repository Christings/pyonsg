from django.shortcuts import render,HttpResponse,redirect
from django.forms.models import model_to_dict
from webqo import models
from fanyi import models as layout
from utils import pagination
import time,json


# Create your views here.


def qo_req(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
	if request.method == 'GET':
		business_lst = layout.Business.objects.all()
		app_lst = layout.Application.objects.all()
		user_app_lst = layout.UserToApp.objects.filter(user_name_id=user_id)
		app_id_lst = list()
		for appid in user_app_lst:
			app_id_lst.append(appid.app_id_id)
		if 6 in app_id_lst:
			return render(request, 'qo_req.html', {'business_lst': business_lst,'user_id':user_id,'user_app_lst':user_app_lst, 'app_lst': app_lst,'businame':'Webqo','app_name':"webqo请求调试"})
		else:
			return render(request, 'no_limit.html',{'business_lst': business_lst,'user_id':user_id,'user_app_lst':user_app_lst, 'app_lst': app_lst,'businame':'Webqo','app_name':"webqo请求调试"})


def qo_task_cancel(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
	ret = {'status': True, 'errro': None, 'data': None}
	try:
		re_add_task_d = request.POST.get('task_id')
		models.webqoqps.objects.filter(id=re_add_task_d).update(status=6)
	except Exception as e:
		ret['error'] = 'error:' + str(e)
		ret['status'] = False
	return HttpResponse(json.dumps(ret))

def qo_task_readd(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
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
		task_detail_todic['status'] = 0
		task_detail_todic['errorlog'] = ""
		task_detail_todic['cost_test'] = ""
		task_detail_todic['cost_base'] = ""
		task_detail_todic['runningIP'] = ""
		task_detail_todic['user'] = user_id
		models.webqoqps.objects.create(**task_detail_todic)
	except Exception as e:
		print(e)
		ret['error'] = 'error:'+str(e)
		ret['status'] = False
	return HttpResponse(json.dumps(ret))


def qo_task_detail(request,task_id):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
	# user_id="zhangjingjun"
	task_detail = models.webqoqps.objects.filter(id=task_id)
	business_lst = layout.Business.objects.all()
	app_lst = layout.Application.objects.all()
	user_app_lst = layout.UserToApp.objects.filter(user_name_id=user_id)
	return render(request, 'qo_task_tail.html',{'business_lst': business_lst, 'app_lst': app_lst, 'user_id':user_id,'user_app_lst':user_app_lst,  'businame': 'Webqo', 'app_name': "webqo性能对比自动化",'topic':'任务详情','task_detail': task_detail})

def qo_automation_add(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
	# user_id = "zhangjingjun"
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
	press_expid = str_dos2unix(request.POST.get('qo_press_expid'))
	press_rate = str_dos2unix(request.POST.get('qo_press_rate'))
	testtag = str_dos2unix(request.POST.get('testtag'))
	print("press_expid", type(press_expid))
	print("press_rate", type(press_rate))
	if press_qps == "":
		press_qps = 1000
	if press_time == "":
		press_time = 30
	if press_expid == "":
		press_expid = 0
	if press_rate == "":
		press_rate = 0
	# print('test_svn:'+test_svn,'base_svn:'+base_svn,'newconfip:'+newconfip,'newconfuser:'+newconfuser,'newconfpassw:'+newconfpassw,'newconfpath:'+newconfpath,'newdataip:'+newdataip,'newdatauser:'+newdatauser,'newdatapassw:'+newdatapassw,'newdatapath:'+newdatapath)
	try:
		models.webqoqps.objects.create(create_time=get_now_time(), user=user_id, testitem=1, testsvn=test_svn,
									   basesvn=base_svn,
									   newconfip=newconfip, newconfuser=newconfuser, newconfpassw=newconfpassw,
									   newconfpath=newconfpath, newdataip=newdataip, newdatauser=newdatauser,
									   newdatapassw=newdatapassw, newdatapath=newdatapath, press_qps=press_qps,
									   press_time=press_time, press_expid=press_expid, press_rate=press_rate,
									   testtag=testtag)
	except Exception as e:
		print(e)
		ret['error'] = 'error:' + str(e)
		ret['status'] = False
	return HttpResponse(json.dumps(ret))


def qo_automation(request, page_id):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
	# user_id="zhangjingjun"

	if page_id == '':
		page_id=1

	task_list = models.webqoqps.objects.order_by('id')[::-1]
	current_page = page_id
	current_page = int(current_page)
	page_obj = pagination.Page(current_page, len(task_list), 16, 9)
	data = task_list[page_obj.start:page_obj.end]
	page_str = page_obj.page_str("/qo_automation")

	business_lst = layout.Business.objects.all()
	app_lst = layout.Application.objects.all()
	user_app_lst = layout.UserToApp.objects.filter(user_name_id=user_id)
	app_id_lst = list()
	for appid in user_app_lst:
		app_id_lst.append(appid.app_id_id)
	if 5 in app_id_lst:
		return render(request, 'qo_automation.html',{'business_lst': business_lst,'user_id':user_id,'user_app_lst':user_app_lst, 'app_lst': app_lst,'businame':'Webqo','app_name':"webqo性能对比自动化",'li':data,'page_str':page_str})
	else:
		return render(request, 'no_limit.html',{'business_lst': business_lst,'user_app_lst':user_app_lst, 'user_id': user_id, 'app_lst': app_lst, 'businame': 'Webqo','app_name': "webqo性能对比自动化"})


def get_now_time():
    timeArray = time.localtime()
    return  time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


def str_dos2unix(input):
    return input.replace('\r\n', '\n').replace(' ', '')

def logout(request):
    response = redirect('https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl=')
    if ('uid' in request.COOKIES):
        response.delete_cookie("uid")
    return response




