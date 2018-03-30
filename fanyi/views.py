from django.shortcuts import render,HttpResponse
from fanyi import models
from fanyi import requestData
import json,requests
# Create your views here.

# fy_automation
def fy_automation(request):
	if request.method == 'GET':
		business_lst = models.Business.objects.all()
		app_lst = models.Application.objects.all()
		req_lst = models.ReqInfo.objects.all()
		timea =models.ReqInfo.objects.all().values()
		# for item in timea:
		# 	print(item)
		return render(request, 'fy_automation.html', {'business_lst': business_lst,'app_lst': app_lst,'businame':'Translate','app_name':"翻译性能对比自动化"})


# allj request
def fy_req_allj(request):
	if request.method == 'GET':
		business_lst = models.Business.objects.all()
		app_lst = models.Application.objects.all()
		req_lst = models.ReqInfo.objects.all()
		timea =models.ReqInfo.objects.all().values()
		# for item in timea:
		# 	print(item)
		return render(request, 'fy_req_allj.html', {'business_lst': business_lst,'app_lst': app_lst,'businame':'Translate','app_name':"JSON请求调试"})

# json request
def fy_req_json(request):
	if request.method == 'GET':
		business_lst = models.Business.objects.all()
		app_lst = models.Application.objects.all()
		req_lst = models.ReqInfo.objects.all()
		timea =models.ReqInfo.objects.all().values()
		# for item in timea:
		# 	print(item)
		return render(request, 'fy_req_json.html', {'business_lst': business_lst,'app_lst': app_lst,'businame':'Translate','app_name':"Alltrans_json请求调试"})

# xml request
def del_xml_line(request):
	ret = {'status': True, 'error': None, 'data': None}
	req_id = request.POST.get('line_id')
	try:
		models.ReqInfo.objects.filter(id=req_id).delete()
	except Exception as e:
		ret['status'] = False
		ret['error'] = "Error:" + str(e)
	return HttpResponse(json.dumps(ret))


def xml_req_save(request):
	ret = {'status': True, 'errro': None, 'data': None}
	inputHost = request.POST.get('inputHost')
	lan_sel = request.POST.get('lan_sel')
	fromto = request.POST.get('inlineRadioOptions')
	reqtext = request.POST.get('reqtext')
	result = request.POST.get('result')
	print(inputHost,lan_sel,fromto,reqtext,result)
	try:
		models.ReqInfo.objects.create(host_ip=inputHost,trans_direct=lan_sel,isfromzh=fromto,req_text=reqtext,result=result,user_fk_id=1)
	except Exception as e:
		ret['error'] = "Error:" + str(e)
		ret['status'] = False
	return HttpResponse(json.dumps(ret))


def xml_req(request):
	ret = {'status': True, 'errro': None, 'data': None}
	inputHost = request.POST.get('inputHost')
	lan_sel = request.POST.get('lan_sel')
	fromto = request.POST.get('inlineRadioOptions')
	reqtext = request.POST.get('reqtext')
	query = requestData.getUniNum(reqtext)
	if fromto == 'tozh':
		fromlan = lan_sel
		tolan = 'zh-CHS'
	else:
		fromlan = 'zh-CHS'
		tolan = lan_sel
	output = 'host={_host},from_lang={_fromlan},to_lang={_tolan},query={_query}'.format(_host=inputHost,_fromlan=fromlan,_tolan=tolan,_query=reqtext)
	print(output)
	data = '''<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v2="http://api.microsofttranslator.com/V2"><soapenv:Header/><soapenv:Body><v2:Translate><v2:appId></v2:appId><v2:debug>true</v2:debug><v2:text>{_reqtext}</v2:text><v2:from>{_fromlan}</v2:from><v2:to>{_tolan}</v2:to><v2:contentType>text/plain</v2:contentType><v2:category>general</v2:category></v2:Translate></soapenv:Body></soapenv:Envelope>'''.format(_reqtext=query,_fromlan=fromlan,_tolan=tolan)
	print(data)
	try:
		resp = requests.post(inputHost, data=data)
		result = requestData.parseXmlRes(resp.text)
		ret['transResult'] = result['transRes']
		ret['debugInfo'] = result['DebugInfo'].replace('<br>','')
		ret['fromlan'] = fromlan
		ret['tolan'] = tolan
		ret['lan_sel'] = lan_sel
		ret['host'] = inputHost
		# print(ret)
	except Exception as e:
		ret['error'] = "Error:"+str(e)
		ret['status'] = False
	return HttpResponse(json.dumps(ret))


def fy_req_xml(request):
	if request.method == 'GET':
		business_lst = models.Business.objects.all()
		app_lst = models.Application.objects.all()
		req_lst = models.ReqInfo.objects.all()
		timea =models.ReqInfo.objects.all().values()
		# for item in timea:
		# 	print(item)
		return render(request, 'fy_req_xml.html', {'business_lst': business_lst,'req_lst':req_lst,'app_lst': app_lst,'businame':'Translate','app_name':"XML请求调试"})



# index
def index(request):
	if request.method == 'GET':
		business_lst = models.Business.objects.all()
		app_lst = models.Application.objects.all()
		return render(request,'layout.html',{'business_lst':business_lst,'app_lst':app_lst})


