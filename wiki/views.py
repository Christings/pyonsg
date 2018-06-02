from django.shortcuts import render,HttpResponse,redirect
from fanyi import models as layout
from wiki import models
from django.db.models import Q
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
		wikidetail = models.Wikistore.objects.filter(id=task_id).values()
		format_md = markdown2.markdown(wikidetail[0]['wikicontent'])
	except Exception as e:
		print(e)
		pass
	return render(request, 'wiki_detail.html',
				  {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
				   'req_lst': req_lst, 'app_lst': app_lst, 'businame': 'wiki', 'topic': 'blog', 'app_name': "wiki detail",
				   'wikidetail':wikidetail,'format_md':format_md})

#wiki list
def wiki_list(request,page_id='1'):
	# login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	# try:
	# 	user_id = request.COOKIES['uid']
	# except:
	# 	return redirect(login_url)
	tag = request.GET.get('tag')
	status = request.GET.get('status')
	search_key = request.GET.get('search_content')
	print('search_key',search_key)
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
		if search_key is not None:
			print(111111111)
			wikilist = models.Wikistore.objects.filter(Q(status=1,wikititle__icontains=search_key)|Q(status=1,wikisummary__icontains=search_key)|Q(status=1,wikicontent__icontains=search_key)|Q(status=1,wikitag__icontains=search_key)|Q(user=user_id,wikititle__icontains=search_key)|Q(user=user_id,wikisummary__icontains=search_key)|Q(user=user_id,wikicontent__icontains=search_key)|Q(user=user_id,wikitag__icontains=search_key)).order_by('update_time')[::-1]
		elif status =='0':
			wikilist = models.Wikistore.objects.filter(user=user_id,status=0).order_by('update_time')[::-1]
		elif tag is None or tag=='all':
			wikilist = models.Wikistore.objects.filter(Q(status=1)|Q(user=user_id)).order_by('update_time')[::-1]
		else:
			wikilist = models.Wikistore.objects.filter(Q(wikitag__icontains=tag,status=1)|Q(user=user_id,wikitag__icontains=tag)).order_by('update_time')[::-1]
		current_page = page_id
		current_page = int(current_page)
		page_obj = pagination.Page(current_page, len(wikilist), 5, 9)
		data = wikilist[page_obj.start:page_obj.end]
		page_str = page_obj.page_str("/wiki_list")
		wikitags = models.Wikistore.objects.filter(Q(status=1)|Q(user=user_id)).values('wikitag')
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
					   'req_lst': req_lst, 'app_lst': app_lst, 'businame': 'wiki','topic':'blog', 'app_name': "wiki list",'li':data,'page_str':page_str,'taglist':taglist})
	else:
		return render(request, 'no_limit.html',
					  {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
					   'req_lst': req_lst, 'app_lst': app_lst, 'businame': 'wiki','topic':'blog', 'app_name': "wiki list"})


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
	flag = request.POST.get('flag')
	try:
		if flag == 'add':
			models.Wikistore.objects.create(create_time=get_now_time(),user=user_id,update_user=user_id,
										update_time=get_now_time(),wikititle=title,wikisummary=summary,wikicontent=content,wikitag=tags,status=1)
		elif flag == 'update':
			id = request.POST.get('edit_id')
			models.Wikistore.objects.filter(id=id).update(update_user=user_id,
											update_time=get_now_time(), wikititle=title, wikisummary=summary,
											wikicontent=content, wikitag=tags, status=1)
		elif flag == 'draft':
			models.Wikistore.objects.create(create_time=get_now_time(), user=user_id, update_user=user_id,
											update_time=get_now_time(), wikititle=title, wikisummary=summary,
											wikicontent=content, wikitag=tags, status=0)
	except Exception as e:
		ret['status']=False
		ret['error']='error:'+str(e)
	return HttpResponse(json.dumps(ret))

#add blog
def edit_blog(request):
	# login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	# try:
	# 	user_id = request.COOKIES['uid']
	# except:
	# 	return redirect(login_url)
	user_id = 'zhangjingjun'
	edit_id = request.GET.get('id')
	try:
		business_lst = layout.Business.objects.all()
		app_lst = layout.Application.objects.all()
		req_lst = layout.ReqInfo.objects.filter(user_fk_id=user_id)
		user_app_lst = layout.UserToApp.objects.filter(user_name_id=user_id)
		app_id_lst = list()
		for appid in user_app_lst:
			app_id_lst.append(appid.app_id_id)
		edit_content = models.Wikistore.objects.filter(id=edit_id).values()
	except Exception as e:
		print(e)
		pass

	if 12 in app_id_lst:
		return render(request, 'wiki_edit_blog.html',
					  {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
					   'req_lst': req_lst, 'app_lst': app_lst, 'businame': 'wiki','topic':'blog', 'app_name': "edit blog",'edit_content':edit_content})
	else:
		return render(request, 'no_limit.html',
					  {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
					   'req_lst': req_lst, 'app_lst': app_lst, 'businame': 'wiki','topic':'blog', 'app_name': "edit blog"})

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

