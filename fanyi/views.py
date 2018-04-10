from django.shortcuts import render,HttpResponse,redirect
from fanyi import models
from fanyi import requestData
from fanyi.models import UserInfo
import json,requests,time,subprocess,urllib.parse
# Create your views here.

# admin
def user_app_del(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
	ret = {'status': True, 'errro': None, 'data': None}
	user_app_id = request.POST.get('user_app_id')
	try:
		nameisExist = models.UserToApp.objects.filter(id=user_app_id)
		if nameisExist.exists() == True:
			nameisExist.delete()
		else:
			ret['error'] = "Error:未找到"
			ret['status'] = False
	except Exception as e:
		ret['error'] = "Error:" + str(e)
		ret['status'] = False
	return HttpResponse(json.dumps(ret))

def sys_user_app(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
	ret = {'status': True, 'errro': None, 'data': None}
	username = request.POST.get('username')
	app_lst = request.POST.getlist('app_lst')
	try:
		for appid in app_lst:
			appisExist = models.UserToApp.objects.filter(user_name_id=username, app_id_id=appid)
			if appisExist.exists() == False:
				models.UserToApp.objects.create(user_name_id=username, app_id_id=appid)
	except Exception as e:
		ret['error'] = "Error:" + str(e)
		ret['status'] = False
	return HttpResponse(json.dumps(ret))



def sys_app_edit(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
	ret = {'status': True, 'errro': None, 'data': None}
	a_id = request.POST.get('app_id')
	b_id = request.POST.get('b_id')
	app_name = request.POST.get('a_name')
	url_name = request.POST.get('url_name')
	print(a_id)
	try:
		nameisExist = models.Application.objects.filter(id=a_id)
		if nameisExist.exists() == True:
			urlisExist = models.Application.objects.filter(urlname=url_name).exclude(id=a_id)
			print(urlisExist.exists())
			if urlisExist.exists() == True:
				ret['error'] = "Error:url已存在"
				ret['status'] = False
			else:
				nameisExist.update(appname=app_name,urlname=url_name,busi_id=b_id)
		else:
			ret['error'] = "Error:未找到"
			ret['status'] = False
	except Exception as e:
		ret['error'] = "Error:" + str(e)
		print(e)
		ret['status'] = False
	return HttpResponse(json.dumps(ret))

def sys_app_del(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
	ret = {'status': True, 'errro': None, 'data': None}
	app_id = request.POST.get('app_id')
	try:
		nameisExist = models.Application.objects.filter(id=app_id)
		if nameisExist.exists() == True:
			app_name = nameisExist.values('urlname')[0]['urlname']
			if app_name=='sys_admin':
				ret['error'] = "Error:无删除权限"
				ret['status'] = False
			else:
				nameisExist.delete()
		else:
			ret['error'] = "Error:未找到"
			ret['status'] = False
	except Exception as e:
		ret['error'] = "Error:" + str(e)
		ret['status'] = False
	return HttpResponse(json.dumps(ret))


def sys_app_add(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
	ret = {'status': True, 'errro': None, 'data': None}
	busi_id = request.POST.get('busi_sel')
	app_name = request.POST.get('app_name')
	url_name = request.POST.get('url_name')
	try:
		urlisExist = models.Application.objects.filter(urlname=url_name)
		if urlisExist.exists() == False:
			models.Application.objects.create(appname=app_name,busi_id=busi_id,urlname=url_name)
		else:
			ret['error'] = "Error:url已存在"
			ret['status'] = False
	except Exception as e:
		ret['error'] = "Error:" + str(e)
		print(e)
		ret['status'] = False
	return HttpResponse(json.dumps(ret))


def sys_busi_edit(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
	ret = {'status': True, 'errro': None, 'data': None}
	b_id = request.POST.get('bid')
	businame = request.POST.get('business_name')
	print(b_id,businame)
	try:
		nameisExist = models.Business.objects.filter(id=b_id)
		if nameisExist.exists() == True:
			nameisExist.update(businame=businame)
		else:
			ret['error'] = "Error:未找到"
			ret['status'] = False
	except Exception as e:
		ret['error'] = "Error:" + str(e)
		print(e)
		ret['status'] = False
	return HttpResponse(json.dumps(ret))

def sys_del_busi(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
	ret = {'status': True, 'errro': None, 'data': None}
	busi_id = request.POST.get('busi_id')
	try:
		nameisExist = models.Business.objects.filter(id=busi_id)

		if nameisExist.exists() == True:
			busi_name = nameisExist.values('businame')[0]['businame']
			if busi_name=='sysadmin':
				ret['error'] = "Error:无删除权限"
				ret['status'] = False
			else:
				nameisExist.delete()
		else:
			ret['error'] = "Error:未找到"
			ret['status'] = False
	except Exception as e:
		ret['error'] = "Error:" + str(e)
		ret['status'] = False
	return HttpResponse(json.dumps(ret))


def sys_add_busi(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
	ret = {'status': True, 'errro': None, 'data': None}
	businame = request.POST.get('business_name')
	try:
		nameisExist = models.Business.objects.filter(businame=businame)
		if nameisExist.exists() == False:

			models.Business.objects.create(businame=businame)
		else:
			ret['error'] = "Error:功能已存在"
			ret['status'] = False
	except Exception as e:
		ret['error'] = "Error:" + str(e)
		print(e)
		ret['status'] = False
	return HttpResponse(json.dumps(ret))

def sys_admin(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
	business_lst = models.Business.objects.all()
	app_lst = models.Application.objects.all()
	utoapp = models.UserToApp.objects.all()
	user_lst = models.UserInfo.objects.all()

	return render(request, 'sys_admin.html',{'business_lst': business_lst, 'app_lst': app_lst,'user_lst':user_lst,'utoapp':utoapp,'businame': 'sysadmin', 'app_name': "系统管理"})




# fy_automation
def fy_automation(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user = request.COOKIES['uid']
	except:
		return redirect(login_url)
	business_lst = models.Business.objects.all()
	app_lst = models.Application.objects.all()
	return render(request, 'fy_automation.html', {'business_lst': business_lst,'app_lst': app_lst,'businame':'Translate','app_name':"翻译性能对比自动化"})


# allj request
def fy_req_allj(request):

	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
	if request.method == 'GET':
		business_lst = models.Business.objects.all()
		app_lst = models.Application.objects.all()

		query=""
		resp = requests.post('http://ywhub01.fy.sjs.ted:12000/alltrans_json', data=query)
		print(resp.text)
		return render(request, 'fy_req_allj.html',{'business_lst': business_lst, 'app_lst': app_lst, 'businame': 'Translate', 'app_name': "alltrans_josn请求调试"})
	# else:
	# 	return render(request, 'fy_req_allj.html',{'business_lst': business_lst, 'app_lst': app_lst, 'businame': 'Translate', 'app_name': "JSON请求调试"})

# json request
def fy_req_json(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
	business_lst = models.Business.objects.all()
	app_lst = models.Application.objects.all()
	req_lst = models.ReqInfo.objects.all()
	timea =models.ReqInfo.objects.all().values()
	# for item in timea:
	# 	print(item)
	return render(request, 'fy_req_json.html', {'business_lst': business_lst,'app_lst': app_lst,'businame':'Translate','app_name':"Alltrans_json请求调试"})

# xml request
def del_xml_line(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except Exception as e:
		return redirect(login_url)
	ret = {'status': True, 'error': None, 'data': None}
	req_id = request.POST.get('line_id')
	try:
		models.ReqInfo.objects.filter(id=req_id).delete()
	except Exception as e:
		ret['status'] = False
		ret['error'] = "Error:" + str(e)
	return HttpResponse(json.dumps(ret))


def xml_req_save(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
	ret = {'status': True, 'errro': None, 'data': None}
	inputHost = request.POST.get('inputHost')
	lan_sel = request.POST.get('lan_sel')
	fromto = request.POST.get('inlineRadioOptions')
	reqtext = request.POST.get('reqtext')
	result = request.POST.get('result')
	reqtype = request.POST.get('reqtype')
	try:
		# models.ReqInfo.objects.create(host_ip=inputHost,trans_direct=lan_sel,isfromzh=fromto,req_text=reqtext,result=result,user_fk_id=user_id)
		models.ReqInfo.objects.create(host_ip=inputHost, trans_direct=lan_sel, isfromzh=fromto, req_text=reqtext,result=result, user_fk_id='user_id',reqtype=reqtype)
		ret['inputHost']=inputHost
		ret['lan_sel']=lan_sel
		ret['fromto']=fromto
		ret['reqtext']=reqtext
		ret['result']=result
		ret['reqtype']=reqtype
	except Exception as e:
		ret['error'] = "Error:" + str(e)
		print(e)
		ret['status'] = False
	return HttpResponse(json.dumps(ret))


def xml_req(request):
	ret = {'status': True, 'errro': None, 'data': None}
	inputHost = request.POST.get('inputHost')
	reqtype = request.POST.get('reqtype')
	lan_sel = request.POST.get('lan_sel')
	fromto = request.POST.get('inlineRadioOptions')
	reqtext = request.POST.get('reqtext')
	# query = requestData.getUniNum(reqtext)
	if fromto == 'tozh':
		fromlan = lan_sel
		tolan = 'zh-CHS'
	else:
		fromlan = 'zh-CHS'
		tolan = lan_sel
	output = 'host={_host},reqtype={_reqtype},from_lang={_fromlan},to_lang={_tolan},query={_query}'.format(_host=inputHost,_reqtype=reqtype,_fromlan=fromlan,_tolan=tolan,_query=reqtext)
	try:
		if reqtype == 'xml':
			xmldata = '''<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v2="http://api.microsofttranslator.com/V2"><soapenv:Header/><soapenv:Body><v2:Translate><v2:appId></v2:appId><v2:debug>true</v2:debug><v2:text>{_reqtext}</v2:text><v2:from>{_fromlan}</v2:from><v2:to>{_tolan}</v2:to><v2:contentType>text/plain</v2:contentType><v2:category>general</v2:category></v2:Translate></soapenv:Body></soapenv:Envelope>'''.format(_reqtext=reqtext, _fromlan=fromlan, _tolan=tolan)
			resp = requests.post(inputHost+'/'+reqtype, data=xmldata.encode('utf-8'))
			result = requestData.parseXmlRes(resp.text)
			ret['transResult'] = result['transRes']
			print(result['DebugInfo'])
			ret['debugInfo'] = result['DebugInfo'].replace('<br>','')
			ret['requestStr'] = xmldata
		elif reqtype == 'alltrans_json':
			prefixq = '''{"to_lang": "'''+tolan+'''"'''+''',"from_lang": "'''+fromlan+'''''''"'''+''',"uuid": "74ad13f3-891c-45f6-99ef-f6de63173a20","sendback": "title"'''+''',"trans_frag": ['''
			suffix=""
			alljquery=""
			temp_len=1
			reqlst = reqtext.split()
			for req in reqlst:
				if temp_len==len(reqlst):
					suffix += '''{"sendback": "title","id":"''' + str(temp_len) + '''","text":"''' + req + '''''''"}]}'''
				else:
					suffix += '''{"sendback": "title","id":"''' + str(temp_len) + '''","text":"''' + req + '''''''"},'''
				temp_len+=1
				alljquery=prefixq+suffix
			resp = requests.post(inputHost + '/' + reqtype, data=alljquery.encode('utf-8'))
			ret['transResult']=requestData.parseAlljRes(resp.text)
			ret['debugInfo'] = resp.text
			ret['requestStr'] = alljquery
		else:
			ret['error'] = "Error:未知的请求类型"
			ret['status'] = False
		ret['fromlan'] = fromlan
		ret['tolan'] = tolan
		ret['lan_sel'] = lan_sel
		ret['host'] = inputHost
		ret['reqtype'] = reqtype
	except Exception as e:
		print(e)
		ret['error'] = "Error:"+str(e)
		ret['status'] = False
	return HttpResponse(json.dumps(ret))


def fy_req_xml(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)

	try:
		business_lst = models.Business.objects.all()
		app_lst = models.Application.objects.all()
		# req_lst = models.ReqInfo.objects.filter(user_fk_id=user_id)
		req_lst = models.ReqInfo.objects.filter(user_fk_id='user_id')
		timea =models.ReqInfo.objects.all().values()
	except Exception as e:
		print(e)
		pass
	return render(request, 'fy_req_xml.html', {'business_lst': business_lst,'req_lst':req_lst,'app_lst': app_lst,'businame':'Translate','app_name':"XML请求调试"})



# index
def index(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
	business_lst = models.Business.objects.all()
	app_lst = models.Application.objects.all()
	return render(request,'layout.html',{'business_lst':business_lst,'app_lst':app_lst})



def home(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	ptoken = ""
	try:
		ptoken = request.GET['ptoken']
	except Exception as e:
		pass
	if ('uid' not in request.COOKIES and ptoken is ""):
		print("no login and not login")
		return redirect(login_url)
	business_lst = models.Business.objects.all()
	app_lst = models.Application.objects.all()
	if (ptoken != ""):#login request callback
		message = urllib.parse.unquote(ptoken)
		child = subprocess.Popen(['/usr/bin/php', '/search/odin/daemon/pyonsg/rsa_decode.php', message], shell = False, stdout = subprocess.PIPE)
		child.wait()
		user = child.stdout.read().decode('utf-8')
		try:
			json_data = json.loads(user)
			uid = json_data['uid']
			login_time = int(json_data['ts'])/1000 #s
			userStatus = models.UserInfo.objects.filter(user_name=uid)
			print(userStatus.exists())
			if userStatus.exists()==False:
				insertInfo = UserInfo(user_name=uid)
				insertInfo.save()
		except Exception as e :
			print(e)
			uid = ""
			login_time = 0
		now_time = time.time()
		print('now_time:',now_time)
		if (uid != "" and now_time - login_time < 60):
			response = render(request, 'layout.html', {'uid': uid,'business_lst':business_lst,'app_lst':app_lst})
			if ('uid' not in request.COOKIES):
				response.set_cookie("uid", uid)
		else:
			print("maybe uid[%s] is empty or now_time[%d] - login_time[%d] >= 60" % (uid, now_time, login_time))
			response = None
	elif ('uid' in request.COOKIES):#already login
		try:
			uid = request.COOKIES['uid']
		except:
			print("should be login, but not login")
			uid = ""
		if (uid != ""):
			response = render(request, 'layout.html', {'business_lst':business_lst,'app_lst':app_lst,'uid': uid})
		else:
			response = None
	if (response == None):
		print("response is none")
		return redirect(login_url)
	return response

