"""pyonsg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from fanyi import views as trans
from webqo import views as webqo
from webqw import views as webqw
from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$',trans.home),
    re_path(r'^sys_admin$',trans.sys_admin),
    re_path(r'^sys_busi_add$',trans.sys_add_busi),
    re_path(r'^sys_busi_del$',trans.sys_del_busi),
    re_path(r'^sys_busi_edit$',trans.sys_busi_edit),
    re_path(r'^sys_app_add$',trans.sys_app_add),
    re_path(r'^sys_app_del$',trans.sys_app_del),
    re_path(r'^sys_app_edit$',trans.sys_app_edit),
    re_path(r'^sys_user_app$',trans.sys_user_app),
    re_path(r'^user_app_del$',trans.user_app_del),
    # xml,json,allj,fy_automation
    re_path(r'^fy_req$',trans.fy_req_xml),
    re_path(r'^xml_req$',trans.xml_req),
    re_path(r'^xml_req_save$',trans.xml_req_save),
    re_path(r'^del_xml_line$',trans.del_xml_line),
    re_path(r'^fy_automation$',trans.fy_automation),
    re_path(r'^fy_bbk$',trans.fy_bbk),
    re_path(r'^fy_bbk_req$',trans.fy_bbk_req),
    # nvi_montor
    re_path(r'^nvidia_smi$',trans.nvidia_smi),
    re_path(r'^montor_host_add$',trans.montor_host_add),
    re_path(r'^del_host_ip',trans.del_host_ip),
    re_path(r'^start_monitor_ip',trans.start_monitor_ip),
    # webqo
    re_path(r'^qo_automation(?P<page_id>\d*)$',webqo.qo_automation),
    re_path(r'^qo_automation_add',webqo.qo_automation_add),
    re_path(r'^qo_task_detail_(?P<task_id>\d+).html$',webqo.qo_task_detail),
    re_path(r'^qo_task_readd$',webqo.qo_task_readd),
    re_path(r'^qo_task_cancel',webqo.qo_task_cancel),
    re_path(r'^qo_req$',webqo.qo_req),
    re_path(r'^logout$',webqo.logout),
    # webqw
    re_path(r'^qw_automation(?P<page_id>\d*)$',webqw.qw_automation),
    re_path(r'^qw_automation_add$',webqw.qw_automation_add),
    re_path(r'^qw_task_detail_(?P<task_id>\d+).html$',webqw.qw_task_detail),
    re_path(r'^qw_task_readd$',webqw.qw_task_readd),
    re_path(r'^qw_task_cancel',webqw.qw_task_cancel),
    re_path(r'^qw_req$',webqw.qw_req),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
