from django.shortcuts import render,HttpResponse,redirect
from fanyi import models as layout
from wiki import models
import json,time,markdown2
from utils import pagination
# Create your views here.


#wiki detail
def wiki_detail(request,task_id):
	# login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	# try:
	# 	user_id = request.COOKIES['uid']
	# except:
	# 	return redirect(login_url)
	try:

		user_id = 'zhangjingjun'
		business_lst = layout.Business.objects.all()
		app_lst = layout.Application.objects.all()
		req_lst = layout.ReqInfo.objects.filter(user_fk_id=user_id)
		user_app_lst = layout.UserToApp.objects.filter(user_name_id=user_id)
		app_id_lst = list()
		for appid in user_app_lst:
			app_id_lst.append(appid.app_id_id)
		#wiki_id = request.GET.get('id')
		wikidetail = models.Wikistore.objects.filter(id=task_id).values()
		#print(wikidetail)
	except Exception as e:
		print(e)
		pass

	return render(request, 'wiki_detail.html',
				  {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
				   'req_lst': req_lst, 'app_lst': app_lst, 'businame': 'wiki', 'topic': 'blog', 'app_name': "add blog",
				   'wikidetail':wikidetail})

#wiki list
def wiki_list(request,page_id='1'):
	# login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	# try:
	# 	user_id = request.COOKIES['uid']
	# except:
	# 	return redirect(login_url)
	tag = request.GET.get('tag')
	print('tag',tag)
	user_id = 'zhangjingjun'
	if page_id == '':
		page_id=1
	try:
		business_lst = layout.Business.objects.all()
		app_lst = layout.Application.objects.all()
		req_lst = layout.ReqInfo.objects.filter(user_fk_id=user_id)
		user_app_lst = layout.UserToApp.objects.filter(user_name_id=user_id)
		app_id_lst = list()
		for appid in user_app_lst:
			app_id_lst.append(appid.app_id_id)

		if tag is None or tag=='all':
			wikilist = models.Wikistore.objects.order_by('update_time')[::-1]
		else:
			wikilist = models.Wikistore.objects.filter(wikitag__icontains=tag).order_by('update_time')[::-1]
		current_page = page_id
		current_page = int(current_page)
		page_obj = pagination.Page(current_page, len(wikilist), 5, 9)
		data = wikilist[page_obj.start:page_obj.end]
		page_str = page_obj.page_str("/wiki_list")
		wikitags = models.Wikistore.objects.all().values('wikitag')
		taglist = list()
		for item in wikitags:
			if '--' in item['wikitag']:
				tagsp = item['wikitag'].split('--')
				taglist += tagsp
			else:
				taglist.append(item['wikitag'])
		taglist=list(set(taglist))

	except Exception as e:
		print(e)
		pass

	if 13 in app_id_lst:
		return render(request, 'wiki_list.html',
					  {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
					   'req_lst': req_lst, 'app_lst': app_lst, 'businame': 'wiki','topic':'blog', 'app_name': "add blog",'li':data,'page_str':page_str,'taglist':taglist})
	else:
		return render(request, 'no_limit.html',
					  {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
					   'req_lst': req_lst, 'app_lst': app_lst, 'businame': 'wiki','topic':'blog', 'app_name': "add blog"})


#save blog
def save_blog(request):
	# login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	# try:
	# 	user_id = request.COOKIES['uid']
	# except:
	# 	return redirect(login_url)
	user_id = 'zhangjingjun'
	ret = {'status': True, 'error': None, 'data': None}
	title = request.POST.get('title')
	summary=request.POST.get('summary')
	content = request.POST.get('content')
	tags = request.POST.get('wikitag')
	try:
		format_md = markdown2.markdown(content)
		print(format_md)
		models.Wikistore.objects.create(create_time=get_now_time(),user=user_id,update_user=user_id,
										update_time=get_now_time(),wikititle=title,wikisummary=summary,wikicontent=format_md,wikitag=tags,status=1)
	except Exception as e:
		ret['status']=False
		ret['error']='error:'+str(e)
	return HttpResponse(json.dumps(ret))

#add blog
def add_blog(request):
	# login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	# try:
	# 	user_id = request.COOKIES['uid']
	# except:
	# 	return redirect(login_url)
	user_id = 'zhangjingjun'

	try:
		business_lst = layout.Business.objects.all()
		app_lst = layout.Application.objects.all()
		req_lst = layout.ReqInfo.objects.filter(user_fk_id=user_id)
		user_app_lst = layout.UserToApp.objects.filter(user_name_id=user_id)
		app_id_lst = list()
		for appid in user_app_lst:
			app_id_lst.append(appid.app_id_id)
	except Exception as e:
		print(e)
		pass

	if 12 in app_id_lst:
		return render(request, 'wiki_add_blog.html',
					  {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
					   'req_lst': req_lst, 'app_lst': app_lst, 'businame': 'wiki','topic':'blog', 'app_name': "add blog"})
	else:
		return render(request, 'no_limit.html',
					  {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
					   'req_lst': req_lst, 'app_lst': app_lst, 'businame': 'wiki','topic':'blog', 'app_name': "add blog"})

def get_now_time():
	timeArray = time.localtime()
	return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

