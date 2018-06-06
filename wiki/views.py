from django.shortcuts import render,HttpResponse,redirect
from fanyi import models as layout
from wiki import models
from django.db.models import Q
from utils import pagination
from utils import resizeImg
import json,time,markdown2,os
# Create your views here.

#del img
def del_img(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except Exception as e:
		return redirect(login_url)
	#user_id = 'zhangjingjun'
	ret = {'status': True, 'error': None, 'data': None}
	img_name = request.POST.get('img_name')
	try:
		# static_dir = '/search/nginx/html/wiki/upload'
		static_dir = 'E:/html/lianxi/img/new/upload'
		user_dir = os.path.join(static_dir, user_id)
		file = os.path.join(user_dir, img_name)
		# print('file',file)
		if os.path.isfile(file):
			os.remove(file)
			big_file = file.split('_rs.')[0]+file.split('_rs.')[1]
			os.remove(big_file)
		# print(big_file)
	except Exception as e:
		ret['status'] = False
		ret['error'] = "Error:" + str(e)
	return HttpResponse(json.dumps(ret))

#upload_img
def upload_img(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
	# user_id = 'zhangjingjun'
	ret = {'status': True, 'error': None, 'data': None}
	obj = request.FILES.get('file')
	if obj:
		try:
			static_dir = '/search/nginx/html/wiki/upload'
			# static_dir = 'E:/html/lianxi/img/new/upload'
			user_dir = os.path.join(static_dir,user_id)
			if os.path.exists(user_dir)==False:
				os.mkdir(user_dir)
			if obj.name in os.listdir(user_dir):
				ret['status'] = False
				ret['error'] = '已存在相同文件名图片'
			else:
				new_file = os.path.join(user_dir,obj.name)
				with open(new_file, 'wb') as fw:
					for chunk in obj.chunks():
						fw.write(chunk)
				prefix_name = obj.name.split('.')[0]
				resize_name = prefix_name+'_rs.'+obj.name.split('.')[1]
				ori_img = new_file
				dst_img = os.path.join(user_dir,resize_name)
				dst_w = 150
				dst_h = 150
				save_q = 35
				resizeImg.resizeImg(ori_img=ori_img, dst_img=dst_img, dst_w=dst_w, dst_h=dst_h, save_q=save_q)
		except Exception as e:
			ret['status'] = False
			ret['error'] = "写入异常" + str(e)
	else:
		ret['status']=False
		ret['error']="未收到文件"
	return HttpResponse(json.dumps(ret))

#wiki img
def wiki_img(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
	# user_id = 'zhangjingjun'
	business_lst = layout.Business.objects.all()
	app_lst = layout.Application.objects.all()
	req_lst = layout.ReqInfo.objects.filter(user_fk_id=user_id)
	user_app_lst = layout.UserToApp.objects.filter(user_name_id=user_id)
	app_id_lst = list()
	for appid in user_app_lst:
		app_id_lst.append(appid.app_id_id)

	static_dir = '/search/nginx/html/wiki/upload'
	#static_dir = 'E:/html/lianxi/img/new/upload'
	user_dir = os.path.join(static_dir, user_id)
	img_lst = list()
	if os.path.exists(user_dir):
		all_img_lst = os.listdir(user_dir)
		for img in all_img_lst:
			if '_rs.' in img:
				img_lst.append(img)
		print(img_lst)

	if 14 in app_id_lst:
		return render(request, 'wiki_img.html',
					  {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
					   'req_lst': req_lst, 'app_lst': app_lst, 'businame': 'wiki','topic':'blog', 'app_name': "wiki list",'img_lst':img_lst})
	else:
		return render(request, 'no_limit.html',
					  {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
					   'req_lst': req_lst, 'app_lst': app_lst, 'businame': 'wiki','topic':'blog', 'app_name': "wiki list"})

#wiki detail
def wiki_detail(request,task_id):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
	# user_id = 'zhangjingjun'
	try:
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

#del wiki
def del_wiki(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except Exception as e:
		return redirect(login_url)
	#user_id = 'zhangjingjun'
	ret = {'status': True, 'error': None, 'data': None}
	req_id = request.POST.get('line_id')
	try:
		models.Wikistore.objects.filter(id=req_id).update(status=2)
	except Exception as e:
		ret['status'] = False
		ret['error'] = "Error:" + str(e)
	return HttpResponse(json.dumps(ret))

#wiki list
def wiki_list(request,page_id='1'):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
	tag = request.GET.get('tag')
	status = request.GET.get('status')
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

		if status =='0':
			wikilist = models.Wikistore.objects.filter(user=user_id,status=0).order_by('update_time')[::-1]
		elif tag is None or tag=='all':
			wikilist = models.Wikistore.objects.exclude(status=2).filter(Q(status=1)|Q(user=user_id)).order_by('update_time')[::-1]
		else:
			wikilist = models.Wikistore.objects.exclude(status=2).filter(Q(wikitag__icontains=tag,status=1)|Q(user=user_id,wikitag__icontains=tag)).order_by('update_time')[::-1]
		current_page = page_id
		current_page = int(current_page)
		page_obj = pagination.Page(current_page, len(wikilist), 5, 9)
		data = wikilist[page_obj.start:page_obj.end]
		page_str = page_obj.page_str("/wiki_list")
		wikitags = models.Wikistore.objects.exclude(status=2).filter(Q(status=1)|Q(user=user_id)).values('wikitag')
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
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
	#user_id = 'zhangjingjun'
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

#edit blog
def edit_blog(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
	# user_id = 'zhangjingjun'
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

		wikitags = models.Wikistore.objects.exclude(status=2).filter(Q(status=1) | Q(user=user_id)).values('wikitag')
		taglist = list()
		for item in wikitags:
			if '--' in item['wikitag']:
				tagsp = item['wikitag'].split('--')
				taglist += tagsp
			else:
				taglist.append(item['wikitag'])
		taglist = list(set(taglist))
	except Exception as e:
		print(e)
		pass

	if 12 in app_id_lst:
		return render(request, 'wiki_edit_blog.html',
					  {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
					   'req_lst': req_lst, 'app_lst': app_lst, 'businame': 'wiki','topic':'blog', 'app_name': "edit blog",'edit_content':edit_content,'taglist':taglist})
	else:
		return render(request, 'no_limit.html',
					  {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
					   'req_lst': req_lst, 'app_lst': app_lst, 'businame': 'wiki','topic':'blog', 'app_name': "edit blog"})

#add blog
def add_blog(request):
	login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
	try:
		user_id = request.COOKIES['uid']
	except:
		return redirect(login_url)
	# user_id = 'zhangjingjun'

	try:
		business_lst = layout.Business.objects.all()
		app_lst = layout.Application.objects.all()
		req_lst = layout.ReqInfo.objects.filter(user_fk_id=user_id)
		user_app_lst = layout.UserToApp.objects.filter(user_name_id=user_id)
		app_id_lst = list()
		for appid in user_app_lst:
			app_id_lst.append(appid.app_id_id)

		wikitags = models.Wikistore.objects.exclude(status=2).filter(Q(status=1) | Q(user=user_id)).values('wikitag')
		taglist = list()
		for item in wikitags:
			if '--' in item['wikitag']:
				tagsp = item['wikitag'].split('--')
				taglist += tagsp
			else:
				taglist.append(item['wikitag'])
		taglist = list(set(taglist))
	except Exception as e:
		print(e)
		pass

	if 12 in app_id_lst:
		return render(request, 'wiki_add_blog.html',
					  {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
					   'req_lst': req_lst, 'app_lst': app_lst, 'businame': 'wiki','topic':'blog', 'app_name': "add blog",'taglist':taglist})
	else:
		return render(request, 'no_limit.html',
					  {'business_lst': business_lst, 'user_id': user_id, 'user_app_lst': user_app_lst,
					   'req_lst': req_lst, 'app_lst': app_lst, 'businame': 'wiki','topic':'blog', 'app_name': "add blog"})

def get_now_time():
	timeArray = time.localtime()
	return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

