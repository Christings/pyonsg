from django.shortcuts import render,HttpResponse,redirect
from django.forms.models import model_to_dict
from fanyi import models
from fanyi import requestData
from fanyi.models import UserInfo
from utils import baidufy_t
from utils import googlefy_t
from utils import youdaofy_t
from utils import qqfy_t
from utils import pagination
import signal,sys
import M2Crypto

import json,requests,time,subprocess,urllib.parse,os,base64
# Create your views here.

def auth(func):
    def inner(request,*args,**kwargs):
        login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
        try:
            user_id = request.COOKIES.get('uid')
            if not user_id:
                return redirect(login_url)
        except:
            return redirect(login_url)
        v = request.COOKIES.get('username111')
        return func(request,*args,**kwargs)
    return inner

# admin
@auth
def user_app_del(request):
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

@auth
def sys_user_app(request):
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


@auth
def sys_app_edit(request):
    ret = {'status': True, 'errro': None, 'data': None}
    a_id = request.POST.get('app_id')
    b_id = request.POST.get('b_id')
    app_name = request.POST.get('a_name')
    url_name = request.POST.get('url_name')
    try:
        nameisExist = models.Application.objects.filter(id=a_id)
        if nameisExist.exists() == True:
            urlisExist = models.Application.objects.filter(urlname=url_name).exclude(id=a_id)
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

@auth
def sys_app_del(request):
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

@auth
def sys_app_add(request):
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

@auth
def sys_busi_edit(request):
    ret = {'status': True, 'errro': None, 'data': None}
    b_id = request.POST.get('bid')
    businame = request.POST.get('business_name')
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

@auth
def sys_del_busi(request):
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

@auth
def sys_add_busi(request):
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

@auth
def sys_admin(request):
    user_id = request.COOKIES.get('uid')
    business_lst = models.Business.objects.all()
    app_lst = models.Application.objects.all()
    utoapp = models.UserToApp.objects.all()
    user_lst = models.UserInfo.objects.all()
    user_app_lst = models.UserToApp.objects.filter(user_name_id=user_id)
    app_id_lst = list()
    for appid in user_app_lst:
        app_id_lst.append(appid.app_id_id)
    if 9 in app_id_lst:
        return render(request, 'sys_admin.html',{'business_lst': business_lst,'user_id':user_id, 'app_lst': app_lst,'user_lst':user_lst,'user_app_lst':user_app_lst,'utoapp':utoapp,'businame': 'sysadmin', 'app_name': "系统管理"})
    else:
        return render(request, 'no_limit.html',{'business_lst': business_lst, 'user_id': user_id, 'app_lst': app_lst, 'user_app_lst':user_app_lst,'businame': 'sysadmin', 'app_name': "系统管理"})


#nvidia
@auth
def del_one_monitor(request):
    ret = {'status': True, 'error': None, 'data': None}
    req_id = request.POST.get('monitor_id')
    try:
        models.FyMonitor.objects.filter(id=req_id).delete()
    except Exception as e:
        ret['status'] = False
        ret['error'] = "Error:" + str(e)
    return HttpResponse(json.dumps(ret))

@auth
def stop_monitor_ip(request):
    ret = {'status': True, 'error': None, 'data': None}
    req_id = request.POST.get('line_id')
    try:
        running_pid = models.Host.objects.filter(id=req_id,status=1).values('runningPID')
        if running_pid:
            for item in running_pid:
                #os.popen('kill -9 %s' % item['runningPID'])
                os.kill(int(item['runningPID']), signal.SIGTERM)
        models.Host.objects.filter(id=req_id).update(runningPID="", status=0)
        models.FyMonitor.objects.filter(status=1, h_id=req_id).update(status=0,end_time=get_now_time())
    except Exception as e:
        ret['status'] = False
        ret['error'] = "Error:" + str(e)
    return HttpResponse(json.dumps(ret))

@auth
def get_nvi_data(request):
    ret = {'status': True, 'error': None, 'gpumem': None,'gpumemused':None}
    fy_nvi_id = request.POST.get('line_id')
    try:
        nvi_data_info = models.FyMonitor.objects.filter(id=fy_nvi_id).first()
        ret['gpumem'] = nvi_data_info.gpumem
        ret['gpumemused'] = nvi_data_info.gpumemused
    except Exception as e:
        ret['status'] = False
        ret['error'] = "Error:" + str(e)
    return HttpResponse(json.dumps(ret))



@auth
def nvi_task_detail(request,task_id):
    # user_id = 'zhangjingjun'
    user_id = request.COOKIES.get('uid')
    task_detail = models.FyMonitor.objects.filter(id=task_id)
    business_lst = models.Business.objects.all()
    app_lst = models.Application.objects.all()
    user_app_lst = models.UserToApp.objects.filter(user_name_id=user_id)
    return render(request, 'nvi_task_detail.html',
                  {'business_lst': business_lst, 'app_lst': app_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
                   'businame': 'Translate', 'app_name': "翻译显存监控", 'topic': '监控详情', 'task_detail': task_detail})

@auth
def start_monitor_ip(request):
    # user_id = 'zhangjingjun'
    user_id = request.COOKIES.get('uid')
    ret = {'status': True, 'error': None, 'data': None}
    req_id = request.POST.get('line_id')
    try:
        running_pid = models.Host.objects.filter(id=req_id,status=1).values('runningPID')
        monitor_ip = models.Host.objects.filter(id=req_id).first()

        if running_pid:
            for item in running_pid:
                os.kill(int(item['runningPID']), signal.SIGTERM)
        close_all_id = models.FyMonitor.objects.filter(status=1, h_id=req_id).values('id')
        for close_id in close_all_id:
            models.FyMonitor.objects.filter(id=close_id['id'], h_id=req_id).update(status=0)
        models.FyMonitor.objects.create(create_time=get_now_time(),monitorip=monitor_ip.ip, user=user_id, status=1, h_id=req_id)
        running_case_id = models.FyMonitor.objects.filter(status=1, h_id=req_id).first()
        os.system('/usr/local/bin/python3 /search/odin/daemon/pyonsg/utils/monitor.py %s %s &' % (str(running_case_id.id),req_id))
        time.sleep(1)
        new_running_ip = models.Host.objects.filter(id=req_id).first()
        if new_running_ip.runningPID=='':
            ret['status'] = False
            ret['error'] = "Error:start error"
            models.FyMonitor.objects.filter(id=running_case_id.id).update(status=2)
    except Exception as e:
        ret['status'] = False
        ret['error'] = "Error:" + str(e)
    return HttpResponse(json.dumps(ret))

@auth
def del_host_ip(request):
    ret = {'status': True, 'error': None, 'data': None}
    req_id = request.POST.get('line_id')
    try:
        models.Host.objects.filter(id=req_id).delete()
    except Exception as e:
        ret['status'] = False
        ret['error'] = "Error:" + str(e)
    return HttpResponse(json.dumps(ret))

@auth
def monitor_host_add(request):
    ret = {'status': True, 'errro': None, 'data': None}
    ip = request.POST.get('monitorip')
    monitor_user = request.POST.get('monitoruser')
    monitor_passw = request.POST.get('monitorpassw')
    gpuid = request.POST.get('gpuid')
    if gpuid =='':
        gpuid = 0
    try:
        nameisExist = models.Host.objects.filter(ip=ip,gpuid=gpuid)
        if nameisExist.exists() == False:
            models.Host.objects.create(ip=ip,user=monitor_user,passw=monitor_passw,gpuid=int(gpuid))
        else:
            ret['error'] = "Error:ip已存在，请勿重新添加"
            ret['status'] = False
    except Exception as e:
        ret['error'] = "Error:" + str(e)
        print(e)
        ret['status'] = False
    return HttpResponse(json.dumps(ret))

@auth
def fy_nvi_iplist(request,task_id,page_id):
    # user_id ='zhangjingjun'
    user_id = request.COOKIES.get('uid')
    if page_id == '':
        page_id = 1
    try:
        business_lst = models.Business.objects.all()
        app_lst = models.Application.objects.all()
        req_lst = models.ReqInfo.objects.filter(user_fk_id=user_id)
        user_app_lst = models.UserToApp.objects.filter(user_name_id=user_id)
        gpu_info = models.FyMonitor.objects.filter(h_id=task_id).values('id', 'create_time', 'end_time', 'monitorip', 'user',
                                                         'status').order_by('id')[::-1]
        current_page = page_id
        current_page = int(current_page)
        page_obj = pagination.Page(current_page, len(gpu_info), 10, 9)
        data = gpu_info[page_obj.start:page_obj.end]
        page_str = page_obj.page_str("/fy_nvi_iplist_%s_" % task_id)

        app_id_lst = list()
        for appid in user_app_lst:
            app_id_lst.append(appid.app_id_id)
    except Exception as e:
        print(e)

    return render(request, 'fy_nvi_iplist.html',
                      {'business_lst': business_lst, 'user_id': user_id,'user_app_lst':user_app_lst,
                       'req_lst': req_lst, 'app_lst': app_lst, 'businame': 'Translate', 'app_name': "翻译比比看",
                       'gpu_info': gpu_info, 'li': data, 'page_str': page_str})
@auth
def nvidia_smi(request,task_id='',page_id=1):
    # user_id = 'zhangjingjun'
    user_id = request.COOKIES.get('uid')
    if page_id == '':
        page_id=1
    try:
        business_lst = models.Business.objects.all()
        app_lst = models.Application.objects.all()
        req_lst = models.ReqInfo.objects.filter(user_fk_id=user_id)
        user_app_lst = models.UserToApp.objects.filter(user_name_id=user_id)
        if task_id=='':
            gpu_info = models.FyMonitor.objects.all().values('id','create_time', 'end_time', 'monitorip', 'user', 'status').order_by('id')[::-1]
        else:
            gpu_info = models.FyMonitor.objects.filter(h_id=task_id).values('id', 'create_time', 'end_time', 'monitorip', 'user',
                                                             'status').order_by('id')[::-1]
        current_page = page_id
        current_page = int(current_page)
        page_obj = pagination.Page(current_page, len(gpu_info), 15, 9)
        data = gpu_info[page_obj.start:page_obj.end]
        page_str = page_obj.page_str("/nvidia_smi_%s_" % task_id)
        host_list = models.Host.objects.all()

        app_id_lst = list()
        for appid in user_app_lst:
            app_id_lst.append(appid.app_id_id)
    except Exception as e:
        print(e)
    if 11 in app_id_lst:
        return render(request, 'fy_nvi_smi.html',
                      {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
                       'req_lst': req_lst, 'app_lst': app_lst, 'businame': 'Translate', 'app_name': "翻译比比看",'gpu_info':gpu_info,'host_list':host_list,'li':data,'page_str':page_str})
    else:
        return render(request, 'no_limit.html',
                      {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
                       'req_lst': req_lst, 'app_lst': app_lst, 'businame': 'Translate', 'app_name': "翻译比比看"})

#fanyi diff unparse xml
@auth
def fy_xmldiff(request):
    # user_id = 'zhangjingjun'
    user_id = request.COOKIES.get('uid')
    page = request.GET.get('page')
    current_page=1
    if page:
        current_page = int(page)

    try:
        task_list = models.FyXmlDiff.objects.order_by('id')[::-1]
        page_obj = pagination.Page(current_page, len(task_list), 16, 9)
        data = task_list[page_obj.start:page_obj.end]
        page_str = page_obj.page_str("/fy_xmldiff?page=")

        business_lst = models.Business.objects.all()
        app_lst = models.Application.objects.all()
        user_app_lst = models.UserToApp.objects.filter(user_name_id=user_id)
        app_id_lst = list()
        for appid in user_app_lst:
            app_id_lst.append(appid.app_id_id)
    except Exception as e:
        print(e)
        pass
    if 18 in app_id_lst:
        return render(request, 'fy_xmldiff.html',
                      {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
                       'app_lst': app_lst, 'businame': 'Translate', 'app_name': "翻译效果对比",'li': data,
                       'page_str': page_str})
    else:
        return render(request, 'no_limit.html',
                      {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
                       'app_lst': app_lst, 'businame': 'Translate', 'app_name': "翻译效果对比"})

@auth
def fy_xmltask_add(request):
    # user_id = "zhangjingjun"
    user_id = request.COOKIES.get('uid')
    ret = {'status': True, 'errro': None, 'data': None}
    test_url = str_dos2unix(request.POST.get('test_url'))
    base_url = str_dos2unix(request.POST.get('base_url'))
    queryip = str_dos2unix(request.POST.get('query_ip'))
    queryuser = str_dos2unix(request.POST.get('query_user'))
    querypassw = str_dos2unix(request.POST.get('query_pass'))
    querypath = str_dos2unix(request.POST.get('query_path'))
    testtag = str_dos2unix(request.POST.get('testtag'))

    try:
        a = models.FyXmlDiff.objects.create(start_time=get_now_time(), user=user_id,test_url=test_url,
                                     base_url=base_url, queryip=queryip,
                                     queryuser=queryuser,
                                     querypassw=querypassw, querypath=querypath,
                                     testtag=testtag)
        os.system('/usr/local/bin/python2 /search/odin/daemon/fanyi/sg_auto_server/lib/getdiff_byxml.py %d &' % a.id)
    except Exception as e:
        ret['error'] = 'error:' + str(e)
        ret['status'] = False
    return HttpResponse(json.dumps(ret))

@auth
def fy_diff_detail(request):
    # user_id="zhangjingjun"
    user_id = request.COOKIES.get('uid')
    task_id = request.GET.get('tasknum')
    task_page = request.GET.get('page')
    page = request.GET.get('page')
    current_page = 1
    if page:
        current_page = int(task_page)

    task_detail = models.FyXmlDiff.objects.filter(id=task_id)
    task_diff_detail = models.XmlDiffContent.objects.filter(diff_task_id=task_id).order_by('id')[::-1]
    page_obj = pagination.Page(current_page, len(task_diff_detail), 4, 9)
    data = task_diff_detail[page_obj.start:page_obj.end]
    page_str = page_obj.page_str("/fy_xmldetail?tasknum="+task_id+'&page=')

    business_lst = models.Business.objects.all()
    app_lst = models.Application.objects.all()
    user_app_lst = models.UserToApp.objects.filter(user_name_id=user_id)

    return render(request, 'fy_diff_detail.html',
                  {'business_lst': business_lst, 'app_lst': app_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
                   'businame': 'Translate', 'app_name': "翻译效果对比", 'topic': '任务详情', 'task_detail': task_detail,'li': data,'page_str': page_str})

@auth
def fy_xml_readd(request):
    user_id = request.COOKIES.get('uid')
    # user_id = "zhangjingjun"
    ret = {'status': True, 'errro': None, 'data': None}
    re_add_task_d = request.POST.get('task_id')
    try:
        task_detail = models.FyXmlDiff.objects.get(id=re_add_task_d)
        task_detail_todic = model_to_dict(task_detail)
        task_detail_todic.pop('id')
        task_detail_todic['create_time'] = get_now_time()
        task_detail_todic['start_time'] =""
        task_detail_todic['end_time'] =""
        task_detail_todic['status'] = 0
        task_detail_todic['errorlog'] = ""
        task_detail_todic['finished'] = 0
        task_detail_todic['user'] = user_id
        models.FyDiff.objects.create(**task_detail_todic)
    except Exception as e:
        print(e)
        ret['error'] = 'error:'+str(e)
        ret['status'] = False
    return HttpResponse(json.dumps(ret))


def fy_cancel_xml(request):
    ret = {'status': True, 'errro': None, 'data': None}
    try:
        re_add_task_d = request.POST.get('task_id')
        res = models.FyXmlDiff.objects.filter(id=re_add_task_d).first()
        models.FyXmlDiff.objects.filter(id=re_add_task_d).update(status=6)
        os.kill(int(res.runningPID), signal.SIGTERM)
        models.FyXmlDiff.objects.filter(id=re_add_task_d).update(status=5, end_time=get_now_time())
    except Exception as e:
        ret['error'] = 'error:' + str(e)
        ret['status'] = False
    return HttpResponse(json.dumps(ret))


#fanyi diff
@auth
def fy_autodiff(request):
    # user_id = 'zhangjingjun'
    user_id = request.COOKIES.get('uid')
    page = request.GET.get('page')
    current_page=1
    if page:
        current_page = int(page)

    try:
        task_list = models.FyDiff.objects.order_by('id')[::-1]
        page_obj = pagination.Page(current_page, len(task_list), 16, 9)
        data = task_list[page_obj.start:page_obj.end]
        page_str = page_obj.page_str("/fy_autodiff?page=")

        business_lst = models.Business.objects.all()
        app_lst = models.Application.objects.all()
        user_app_lst = models.UserToApp.objects.filter(user_name_id=user_id)
        app_id_lst = list()
        for appid in user_app_lst:
            app_id_lst.append(appid.app_id_id)
    except Exception as e:
        print(e)
        pass
    if 17 in app_id_lst:
        return render(request, 'fy_autodiff.html',
                      {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
                       'app_lst': app_lst, 'businame': 'Translate', 'app_name': "翻译效果对比",'li': data,
                       'page_str': page_str})
    else:
        return render(request, 'no_limit.html',
                      {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
                       'app_lst': app_lst, 'businame': 'Translate', 'app_name': "翻译效果对比"})

@auth
def fy_difftask_add(request):
    user_id = "zhangjingjun"
    # user_id = request.COOKIES.get('uid')
    ret = {'status': True, 'errro': None, 'data': None}
    hubsvn = str_dos2unix(request.POST.get('hub_svn'))
    sersvn = str_dos2unix(request.POST.get('server_svn'))
    hubcfgip = str_dos2unix(request.POST.get('hub_conf_ip'))
    hubcfguser = str_dos2unix(request.POST.get('hub_conf_user'))
    hubcfgpassw = str_dos2unix(request.POST.get('hub_conf_pass'))
    hubcfgpath = str_dos2unix(request.POST.get('hub_conf_path'))
    hubdatapath = str_dos2unix(request.POST.get('hub_data_path'))
    sercfgip = str_dos2unix(request.POST.get('ser_conf_ip'))
    sercfguser = str_dos2unix(request.POST.get('ser_conf_user'))
    sercfgpassw = str_dos2unix(request.POST.get('ser_conf_pass'))
    sercfgpath = str_dos2unix(request.POST.get('ser_conf_path'))
    serdatapath = str_dos2unix(request.POST.get('ser_data_path'))
    queryip = str_dos2unix(request.POST.get('query_ip'))
    queyruser = str_dos2unix(request.POST.get('query_user'))
    querypassw = str_dos2unix(request.POST.get('query_pass'))
    querypath = str_dos2unix(request.POST.get('query_path'))
    testtag = str_dos2unix(request.POST.get('testtag'))
    lan_sel = request.POST.get('lan_sel')
    fromto = request.POST.get('inlineRadioOptions')
    if fromto == 'tozh':
        fromlan = lan_sel
        tolan = 'zh-CHS'
    else:
        fromlan = 'zh-CHS'
        tolan = lan_sel

    try:
        models.FyDiff.objects.create(create_time=get_now_time(), user=user_id,hubsvn=hubsvn,
                                       sersvn=sersvn,
                                       hubcfgip=hubcfgip, hubcfguser=hubcfguser,
                                       hubcfgpassw=hubcfgpassw, hubcfgpath=hubcfgpath, hubdatapath=hubdatapath,
                                       sercfgip=sercfgip, sercfguser=sercfguser, sercfgpassw=sercfgpassw,
                                       sercfgpath=sercfgpath, serdatapath=serdatapath, queryip=queryip,queyruser=queyruser,
                                       querypassw=querypassw,querypath=querypath,
                                       testtag=testtag,fromlan=fromlan,tolan=tolan,lan_sel=lan_sel, isfromzh=fromto)
    except Exception as e:
        print(e)
        ret['error'] = 'error:' + str(e)
        ret['status'] = False
    return HttpResponse(json.dumps(ret))

@auth
def fy_task_detail(request):
    # user_id="zhangjingjun"
    user_id = request.COOKIES.get('uid')
    task_id = request.GET.get('tasknum')
    task_page = request.GET.get('page')
    page = request.GET.get('page')
    current_page = 1
    if page:
        current_page = int(task_page)

    task_detail = models.FyDiff.objects.filter(id=task_id)
    task_diff_detail = models.DiffContent.objects.filter(diff_task_id=task_id).order_by('id')[::-1]
    page_obj = pagination.Page(current_page, len(task_diff_detail), 4, 9)
    data = task_diff_detail[page_obj.start:page_obj.end]
    page_str = page_obj.page_str("/fy_task_detail?tasknum="+task_id+'&page=')

    business_lst = models.Business.objects.all()
    app_lst = models.Application.objects.all()
    user_app_lst = models.UserToApp.objects.filter(user_name_id=user_id)

    return render(request, 'fy_task_tail.html',
                  {'business_lst': business_lst, 'app_lst': app_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
                   'businame': 'Translate', 'app_name': "翻译效果对比", 'topic': '任务详情', 'task_detail': task_detail,'li': data,'page_str': page_str})

@auth
def fy_task_readd(request):
    user_id = request.COOKIES.get('uid')
    # user_id = "zhangjingjun"
    ret = {'status': True, 'errro': None, 'data': None}
    re_add_task_d = request.POST.get('task_id')
    try:
        task_detail = models.FyDiff.objects.get(id=re_add_task_d)
        task_detail_todic = model_to_dict(task_detail)
        task_detail_todic.pop('id')
        task_detail_todic['create_time'] = get_now_time()
        task_detail_todic['start_time'] =""
        task_detail_todic['end_time'] =""
        task_detail_todic['status'] = 0
        task_detail_todic['errorlog'] = ""
        task_detail_todic['finished'] = 0
        task_detail_todic['runningIP'] = ""
        task_detail_todic['user'] = user_id
        models.FyDiff.objects.create(**task_detail_todic)
    except Exception as e:
        print(e)
        ret['error'] = 'error:'+str(e)
        ret['status'] = False
    return HttpResponse(json.dumps(ret))


def fy_task_cancel(request):
    ret = {'status': True, 'errro': None, 'data': None}
    try:
        re_add_task_d = request.POST.get('task_id')
        models.FyDiff.objects.filter(id=re_add_task_d).update(status=6)
    except Exception as e:
        ret['error'] = 'error:' + str(e)
        ret['status'] = False
    return HttpResponse(json.dumps(ret))

def get_now_time():
    timeArray = time.localtime()
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

def str_dos2unix(input):
    return input.replace('\r\n', '\n').replace(' ', '')

#bbk

def fy_bbk_req(request):
    ret = {'status': True, 'errro': None, 'data': None}
    inputHost = request.POST.get('inputHost')
    reqtype = request.POST.get('reqtype')
    lan_sel = request.POST.get('lan_sel')
    fromto = request.POST.get('inlineRadioOptions')
    reqtext = request.POST.get('reqtext')
    if fromto == 'tozh':
        fromlan = lan_sel
        tolan = 'zh-CHS'
    else:
        fromlan = 'zh-CHS'
        tolan = lan_sel
    # output = 'host={_host},reqtype={_reqtype},from_lang={_fromlan},to_lang={_tolan},query={_query}'.format(_host=inputHost, _reqtype=reqtype, _fromlan=fromlan, _tolan=tolan, _query=reqtext)
    sg_begin=time.time()


    try:
        if reqtype == 'xml':
            xmldata = '''<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v2="http://api.microsofttranslator.com/V2"><soapenv:Header/><soapenv:Body><v2:Translate><v2:appId></v2:appId><v2:debug>true</v2:debug><v2:text>{_reqtext}</v2:text><v2:from>{_fromlan}</v2:from><v2:to>{_tolan}</v2:to><v2:contentType>text/plain</v2:contentType><v2:category>general</v2:category></v2:Translate></soapenv:Body></soapenv:Envelope>'''.format(
                _reqtext=reqtext, _fromlan=fromlan, _tolan=tolan)
            resp = requests.post(inputHost + '/' + reqtype, data=xmldata.encode('utf-8'))
            result = requestData.parseXmlRes(resp.text)
            ret['transResult'] = result['transRes']
            ret['reqtype'] = 'xml'
        elif reqtype == 'alltrans_json':
            prefixq = '''{"to_lang": "''' + tolan + '''"''' + ''',"from_lang": "''' + fromlan + '''''''"''' + ''',"uuid": "74ad13f3-891c-45f6-99ef-f6de63173a20","sendback": "title"''' + ''',"trans_frag": ['''
            suffix = ""
            alljquery = ""
            temp_len = 1
            reqlst = reqtext.split('\r\n')
            for req in reqlst:
                if temp_len == len(reqlst):
                    suffix += '''{"sendback": "title","id":"''' + str(
                        temp_len) + '''","text":"''' + req + '''''''"}]}'''
                else:
                    suffix += '''{"sendback": "title","id":"''' + str(temp_len) + '''","text":"''' + req + '''''''"},'''
                temp_len += 1
                alljquery = prefixq + suffix
            resp = requests.post(inputHost + '/' + reqtype, data=alljquery.encode('utf-8'))
            ret['transResult'] = requestData.parseAlljRes(resp.text)
            ret['reqtype'] = 'alltrans_json'
        else:
            ret['error'] = "Error:未知的请求类型"
            ret['status'] = False
        sg_end=time.time()
        other_begin=time.time()
        threads = []
        # Baidu
        t_bd = baidufy_t.bdThread(target=baidufy_t.getResult_bd, args=(fromlan, tolan, reqtext))
        threads.append(t_bd)
        # google 接口失效
        # t_gg = googlefy_t.ggThread(target=googlefy_t.getResult_gg, args=(fromlan, tolan, reqtext))
        # threads.append(t_gg)
        # QQ
        t_qq = qqfy_t.qqThread(target=qqfy_t.getResult_qq, args=(fromlan, tolan, reqtext))
        threads.append(t_qq)
        # youdao
        t_yd = youdaofy_t.ydThread(target=youdaofy_t.getResult_yd, args=(fromlan, tolan, reqtext))
        threads.append(t_yd)

        for thead_id in range(len(threads)):
            threads[thead_id].start()

        ret['bd_result'] = threads[0].join()
        # ret['gg_result'] = threads[1].join()
        ret['qq_result'] = threads[1].join()
        ret['yd_result'] = threads[2].join()
        other_end = time.time()
        ret['fromlan'] = fromlan
        ret['tolan'] = tolan
        ret['lan_sel'] = lan_sel
        ret['host'] = inputHost
        sg_cost=sg_end-sg_begin
        other_cost = other_end-other_begin
        print('sg_cost',sg_cost)
        print('other_cost',other_cost)
    except Exception as e:
        print(e)
        ret['error'] = "Error:" + str(e)
        ret['status'] = False
    return HttpResponse(json.dumps(ret))

@auth
def fy_bbk(request):
    user_id = 'zhangjingjun'
    # user_id = request.COOKIES.get('uid')
    try:
        business_lst = models.Business.objects.all()
        app_lst = models.Application.objects.all()
        req_lst = models.ReqInfo.objects.filter(user_fk_id=user_id)
        user_app_lst = models.UserToApp.objects.filter(user_name_id=user_id)
        app_id_lst = list()
        for appid in user_app_lst:
            app_id_lst.append(appid.app_id_id)
    except Exception as e:
        print(e)
        pass
    if 10 in app_id_lst:
        return render(request, 'fy_bbk.html', {'business_lst': business_lst,'user_id':user_id,'user_app_lst':user_app_lst,'req_lst':req_lst,'app_lst': app_lst,'businame':'Translate','app_name':"翻译比比看"})
    else:
        return render(request, 'no_limit.html',{'business_lst': business_lst, 'user_id': user_id,'user_app_lst':user_app_lst, 'req_lst': req_lst, 'app_lst': app_lst,'businame': 'Translate', 'app_name': "翻译比比看"})


# fy_automation
@auth
def fy_automation(request):
    # user_id = 'zhangjingjun'
    user_id = request.COOKIES.get('uid')
    business_lst = models.Business.objects.all()
    app_lst = models.Application.objects.all()
    user_app_lst = models.UserToApp.objects.filter(user_name_id=user_id)
    app_id_lst = list()
    for appid in user_app_lst:
        app_id_lst.append(appid.app_id_id)
    if 4 in app_id_lst:
        return render(request, 'fy_automation.html', {'business_lst': business_lst,'user_id':user_id,'user_app_lst':user_app_lst,'app_lst': app_lst,'businame':'Translate','app_name':"翻译性能对比自动化"})
    else:
        return render(request, 'no_limit.html',{'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,'app_lst': app_lst, 'businame': 'Translate', 'app_name': "翻译性能对比自动化"})


# xml request
@auth
def del_xml_line(request):
    ret = {'status': True, 'error': None, 'data': None}
    req_id = request.POST.get('line_id')
    try:
        models.ReqInfo.objects.filter(id=req_id).delete()
    except Exception as e:
        ret['status'] = False
        ret['error'] = "Error:" + str(e)
    return HttpResponse(json.dumps(ret))

@auth
def xml_req_save(request):
    # user_id = 'zhangjingjun'
    user_id = request.COOKIES.get('uid')
    ret = {'status': True, 'errro': None, 'data': None}
    inputHost = request.POST.get('inputHost')
    lan_sel = request.POST.get('lan_sel')
    fromto = request.POST.get('inlineRadioOptions')
    reqtext = request.POST.get('reqtext')
    result = request.POST.get('result')
    if result is None:
        result=""
    reqtype = request.POST.get('reqtype')
    try:
        models.ReqInfo.objects.create(host_ip=inputHost, trans_direct=lan_sel, isfromzh=fromto, req_text=reqtext,result=result, user_fk_id=user_id,reqtype=reqtype)
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
    # print(reqtext)
    query = requestData.getUniNum(reqtext)
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

@auth
def fy_req_xml(request):
    # user_id = 'zhangjingjun'
    user_id = request.COOKIES['uid']
    try:
        business_lst = models.Business.objects.all()
        app_lst = models.Application.objects.all()
        req_lst = models.ReqInfo.objects.filter(user_fk_id=user_id)
        user_app_lst = models.UserToApp.objects.filter(user_name_id=user_id)
        app_id_lst = list()
        for appid in user_app_lst:
            app_id_lst.append(appid.app_id_id)
    except Exception as e:
        print(e)
        pass
    if 3 in app_id_lst:
        return render(request, 'fy_req_xml.html', {'business_lst': business_lst,'user_id':user_id,'user_app_lst':user_app_lst,'req_lst':req_lst,'app_lst': app_lst,'businame':'Translate','app_name':"请求调试"})
    else:
        return render(request, 'no_limit.html',{'business_lst': business_lst, 'user_id': user_id,'user_app_lst':user_app_lst, 'req_lst': req_lst, 'app_lst': app_lst,'businame': 'Translate', 'app_name': "请求调试"})


def home(request):
    login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
    ptoken = ""
    try:
        ptoken = request.GET['ptoken']
    except Exception as e:
        pass
    if ('uid' not in request.COOKIES and ptoken is ""):
        return redirect(login_url)
    business_lst = models.Business.objects.all()
    app_lst = models.Application.objects.all()

    if (ptoken != ""):#login request callback
        message = urllib.parse.unquote(ptoken)
        # login with php
        # child = subprocess.Popen(['/usr/bin/php', '/search/odin/daemon/pyonsg/rsa_decode.php', message], shell = False, stdout = subprocess.PIPE)
        # child.wait()
        # user = child.stdout.read().decode('utf-8')
        # login with phthon
        strcode = base64.b64decode(message)
        pkey = M2Crypto.RSA.load_pub_key('/search/odin/daemon/pyonsg/public.pem')
        output = pkey.public_decrypt(strcode, M2Crypto.RSA.pkcs1_padding)
        try:
            json_data = json.loads(output.decode('utf-8'))
            uid = json_data['uid']
            login_time = int(json_data['ts'])/1000 #s
            userStatus = models.UserInfo.objects.filter(user_name=uid)
            if userStatus.exists()==False:
                insertInfo = UserInfo(user_name=uid)
                insertInfo.save()
        except Exception as e :
            print(e)
            uid = ""
            login_time = 0
        now_time = time.time()
        if (uid != "" and now_time - login_time < 60):
            user_app_lst = models.UserToApp.objects.filter(user_name_id=uid)
            response = render(request, 'layout.html', {'uid_id': uid,'user_app_lst':user_app_lst, 'business_lst':business_lst,'app_lst':app_lst})
            if ('uid' not in request.COOKIES):
                response.set_cookie("uid", uid)
        else:
            response = None
    elif ('uid' in request.COOKIES):#already login
        try:
            uid = request.COOKIES['uid']
        except:
            uid = ""
        if (uid != ""):
            user_app_lst = models.UserToApp.objects.filter(user_name_id=uid)
            response = render(request, 'layout.html', {'business_lst':business_lst,'app_lst':app_lst,'uid_id': uid,'user_app_lst':user_app_lst})
        else:
            response = None
    if (response == None):
        return redirect(login_url)
    return response



def test_xml(request):
    import random
    temp_num = random.randint(1,10)
    query_str = request.GET.get('key')
    result_str=query_str+str(temp_num)
    xml_str = """
    <data>
    <request name="Sogou">
        <rank>1</rank>
        <year>2008</year>
        <qtext>hello world</qtext>
    </request>
    <result name="Sogou">
        <rank>1</rank>
        <year>2008</year>
        <qresult>"""+result_str+"""</qresult>
    </result>
    </data>"""
    return HttpResponse(xml_str)

# models bleu
# @auth
def models_bleu(request):
    user_id = 'zhangjingjun'
    # user_id = request.COOKIES.get('uid')
    if request.method == 'GET':
        page = request.GET.get('page')
        current_page=1
        if page:
            current_page = int(page)

        try:
            task_list = models.FyXmlDiff.objects.order_by('id')[::-1]
            page_obj = pagination.Page(current_page, len(task_list), 16, 9)
            data = task_list[page_obj.start:page_obj.end]
            page_str = page_obj.page_str("/fy_xmldiff?page=")

            business_lst = models.Business.objects.all()
            app_lst = models.Application.objects.all()
            user_app_lst = models.UserToApp.objects.filter(user_name_id=user_id)
            app_id_lst = list()
            for appid in user_app_lst:
                app_id_lst.append(appid.app_id_id)
        except Exception as e:
            print(e)
            pass
        print(app_id_lst)
        if 19 in app_id_lst:

            return render(request, 'models_bleu.html',
                          {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
                           'app_lst': app_lst, 'businame': 'Translate', 'app_name': "翻译效果对比",'li': data,
                           'page_str': page_str})
        else:
            return render(request, 'no_limit.html',
                          {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
                           'app_lst': app_lst, 'businame': 'Translate', 'app_name': "翻译效果对比"})
    elif request.method == 'POST':
        pass
