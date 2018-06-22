from django.shortcuts import render, HttpResponse, redirect
from django.forms.models import model_to_dict
from webqw import models
from fanyi import models as layout
from utils import pagination
import time, json
import requests
from requests import Request
from urllib.parse import urlencode
import sys
from bs4 import BeautifulSoup


# Create your views here.

def auth(func):
    def inner(request, *args, **kwargs):
        # login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
        # try:
        #     user_id = request.COOKIES.get('uid')
        #     if not user_id:
        #         return redirect(login_url)
        # except:
        #     return redirect(login_url)
        # v = request.COOKIES.get('username111')
        return func(request, *args, **kwargs)

    return inner


@auth
def qw_req(request):
    user_id = "zhangjingjun"
    # user_id = request.COOKIES.get('uid')
    if request.method == 'GET':
        business_lst = layout.Business.objects.all()
        app_lst = layout.Application.objects.all()
        req_lst = models.ReqInfo_QW.objects.filter(user_fk_id=user_id)
        user_app_lst = layout.UserToApp.objects.filter(user_name_id=user_id)
        app_id_lst = list()
        for appid in user_app_lst:
            app_id_lst.append(appid.app_id_id)
        if 8 in app_id_lst:
            return render(request, 'qw_req.html',
                          {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
                           'req_lst': req_lst,
                           'app_lst': app_lst, 'businame': 'Webqw', 'app_name': "webqw请求调试"})
        else:
            return render(request, 'no_limit.html',
                          {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
                           'req_lst': req_lst,
                           'app_lst': app_lst, 'businame': 'Webqw', 'app_name': "webqw请求调试"})


def qw_req_info(request):
    user_id = "zhangjingjun"
    ret = {
        'status': True,
        'error': None,
        'data': None
    }
    inputHost = request.POST.get('inputHost')
    # reqtype = request.POST.get('reqtype')
    inputExpId = request.POST.get('inputExpId')
    query = request.POST.get('reqtext')

    exp_id = inputExpId + "^0^0^0^0^0^0^0^0"
    exp_id = exp_id.encode('utf-16LE')

    utf16_query = query.encode('utf-16LE', 'ignore')

    params = urlencode({
        'queryString': utf16_query,
        'forceQuery': 1,
        'exp_id': exp_id,
    })

    headers = {"Content-type": "application/x-www-form-urlencoded;charset=UTF-16LE"}

    try:
        resp = requests.post(inputHost, data=params, headers=headers)
        status = resp.reason
        if status != 'OK':
            print(sys.stderr, query, status)
            ret['error'] = 'Error:未知的请求类型'
            ret['status'] = False
            return ret
        data = BeautifulSoup(resp.text)
        ret['data'] = data.prettify()

    except Exception as e:
        print(e)
        print(sys.stderr, sys.exc_info()[0], sys.exc_info()[1])
        print(sys.stderr, query)
        ret['error'] = "Error:" + str(e)
        ret['status'] = False
    return HttpResponse(json.dumps(ret))


@auth
def qw_req_del(request):
    ret = {'status': True, 'error': None, 'data': None}
    req_id = request.POST.get('line_id')
    try:
        models.ReqInfo_QW.objects.filter(id=req_id).delete()
    except Exception as e:
        ret['status'] = False
        ret['error'] = "Error:" + str(e)
        print(e)
    return HttpResponse(json.dumps(ret))


@auth
def qw_req_save(request):
    user_id = "zhangjingjun"
    ret = {
        'status': True,
        'error': None,
        'data': None,
    }
    inputHost = request.POST.get('inputHost')
    # reqtype=request.POST.get('reqtype')
    inputExpId = request.POST.get('inputExpId')
    query = request.POST.get('reqtext')
    # result = request.POST.get('result')

    try:
        models.ReqInfo_QW.objects.create(host_ip=inputHost, exp_id=inputExpId, req_text=query,
                                         user_fk_id=user_id)
        ret['inputHost'] = inputHost
        ret['inputExpId'] = inputExpId
        ret['query'] = query
    except Exception as e:
        ret['error'] = "Error:" + str(e)
        print(e)
        ret['status'] = False
    return HttpResponse(json.dumps(ret))


@auth
def qw_task_cancel(request):
    ret = {'status': True, 'errro': None, 'data': None}
    try:
        re_add_task_d = request.POST.get('task_id')
        models.webqwqps.objects.filter(id=re_add_task_d).update(status=6)
    except Exception as e:
        ret['error'] = 'error:' + str(e)
        ret['status'] = False
    return HttpResponse(json.dumps(ret))


@auth
def qw_task_readd(request):
    user_id = request.COOKIES.get('uid')
    ret = {'status': True, 'errro': None, 'data': None}
    re_add_task_d = request.POST.get('task_id')
    try:
        task_detail = models.webqwqps.objects.get(id=re_add_task_d)
        task_detail_todic = model_to_dict(task_detail)
        task_detail_todic.pop('id')
        task_detail_todic['create_time'] = get_now_time()
        task_detail_todic['start_time'] = ""
        task_detail_todic['end_time'] = ""
        task_detail_todic['testitem'] = 1
        task_detail_todic['status'] = 0
        task_detail_todic['errorlog'] = ""
        task_detail_todic['cost_test'] = ""
        task_detail_todic['cost_base'] = ""
        task_detail_todic['runningIP'] = ""
        task_detail_todic['user'] = user_id
        models.webqwqps.objects.create(**task_detail_todic)
    except Exception as e:
        print(e)
        ret['error'] = 'error:' + str(e)
        ret['status'] = False
    return HttpResponse(json.dumps(ret))


@auth
def qw_task_detail(request, task_id):
    # user_id="zhangjingjun"
    user_id = request.COOKIES.get('uid')
    task_detail = models.webqwqps.objects.filter(id=task_id)
    business_lst = layout.Business.objects.all()
    app_lst = layout.Application.objects.all()
    user_app_lst = layout.UserToApp.objects.filter(user_name_id=user_id)
    return render(request, 'qw_task_tail.html',
                  {'business_lst': business_lst, 'app_lst': app_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
                   'businame': 'Webqw', 'app_name': "webqw性能对比自动化", 'topic': '任务详情', 'task_detail': task_detail})


@auth
def qw_automation_add(request):
    # user_id = "zhangjingjun"
    user_id = request.COOKIES.get('uid')
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
    press_expid = str_dos2unix(request.POST.get('qw_press_expid'))
    press_rate = str_dos2unix(request.POST.get('qw_press_rate'))
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
        models.webqwqps.objects.create(create_time=get_now_time(), user=user_id, testitem=1, testsvn=test_svn,
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


@auth
def qw_automation(request, page_id):
    # user_id="zhangjingjun"
    user_id = request.COOKIES.get('uid')
    if page_id == '':
        page_id = 1
    task_list = models.webqwqps.objects.order_by('id')[::-1]

    current_page = page_id
    current_page = int(current_page)
    page_obj = pagination.Page(current_page, len(task_list), 16, 9)
    data = task_list[page_obj.start:page_obj.end]
    page_str = page_obj.page_str("/qw_automation")

    business_lst = layout.Business.objects.all()
    app_lst = layout.Application.objects.all()
    user_app_lst = layout.UserToApp.objects.filter(user_name_id=user_id)
    app_id_lst = list()
    for appid in user_app_lst:
        app_id_lst.append(appid.app_id_id)
    if 7 in app_id_lst:
        return render(request, 'qw_automation.html',
                      {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
                       'app_lst': app_lst, 'businame': 'Webqw', 'app_name': "webqw性能对比自动化", 'li': data,
                       'page_str': page_str})
    else:
        return render(request, 'no_limit.html',
                      {'business_lst': business_lst, 'user_app_lst': user_app_lst, 'user_id': user_id,
                       'app_lst': app_lst, 'businame': 'Webqw', 'app_name': "webqw性能对比自动化"})


def get_now_time():
    timeArray = time.localtime()
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


def str_dos2unix(input):
    return input.replace('\r\n', '\n').replace(' ', '')
