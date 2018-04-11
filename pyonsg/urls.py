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
    # xml
    re_path(r'^index$',trans.index),
    re_path(r'^fy_req$',trans.fy_req_xml),
    re_path(r'^xml_req$',trans.xml_req),
    re_path(r'^xml_req_save$',trans.xml_req_save),
    re_path(r'^del_xml_line$',trans.del_xml_line),
    # json
    re_path(r'^fy_req_json$',trans.fy_req_json),
    # allj
    re_path(r'^fy_req_allj$',trans.fy_req_allj),
    # fy_automation
    re_path(r'^fy_automation$',trans.fy_automation),
    # webqo
    re_path(r'^qo_automation$',webqo.qo_automation),
    re_path(r'^qo_req$',webqo.qo_req),
    # webqo
    re_path(r'^qw_automation$',webqw.qw_automation),
    re_path(r'^qw_req$',webqw.qw_req),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
