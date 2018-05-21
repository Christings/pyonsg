#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'zhangjingjun'
__mtime__ = '2018/5/17'
# ----------Dragon be here!----------
              ┏━┓      ┏━┓
            ┏━┛ ┻━━━━━━┛ ┻━━┓
            ┃       ━       ┃
            ┃  ━┳━┛   ┗━┳━  ┃
            ┃       ┻       ┃
            ┗━━━┓      ┏━━━━┛
                ┃      ┃神兽保佑
                ┃      ┃永无BUG！
                ┃      ┗━━━━━━━━━┓
                ┃                ┣━┓
                ┃                ┏━┛
                ┗━━┓ ┓ ┏━━━┳━┓ ┏━┛
                   ┃ ┫ ┫   ┃ ┫ ┫
                   ┗━┻━┛   ┗━┻━┛
"""
import html.parser
import urllib.request
import urllib.parse
import re
import html
import requests
import json
class Googlefy:
	def __init__(self):
		self.agent = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36",'Host': 'www.googleapis.com','Connection': 'keep-alive','Cache-Control': 'max-age=0','Upgrade-Insecure-Requests': '1','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','X-Client-Data': 'CI22yQEIorbJAQjEtskBCKmdygEIqKPKARismMoB','Accept-Encoding': 'gzip, deflate, br','Accept-Language': 'zh-CN,zh;q=0.9'}

	def unescape(self, text):
		return (html.unescape(text))

	# 页面抓取方式的翻译api，抓取无线端的翻译结果
	def TranslateByGoogle(self, text, fromLang, toLang):
		base_link = "http://translate.google.cn/m?hl=%s&sl=%s&q=%s"
		text = urllib.parse.quote(text)
		link = base_link % (toLang, fromLang, text)
		req = urllib.request.Request(link, headers=self.agent)
		try:
			raw_data = urllib.request.urlopen(req).read()
			print(str(raw_data,encoding="utf-8"))
			data = raw_data.decode("utf-8")
			expr = r'class="t0">(.*?)<'
			re_result = re.findall(expr, data)
			if (len(re_result) == 0):
				result = ""
			else:
				result = html.unescape(re_result[0])
			return (result)
		except Exception as e:
			print(e)
	def TranslateByGgapi(self, text, fromLang, toLang):
		myurl = "https://www.googleapis.com/language/translate/v2?key=AIzaSyAXbOYLde61UfNKXqVADyXOFkmWvamjJQc&source=%s&target=%s&q=%s" % (fromLang, toLang, urllib.parse.quote(text))
		url = 'http://wget.task.gd.ted/wget.php?url='+urllib.parse.quote(myurl)
		resp = requests.get(url,headers=self.agent)
		#resp = requests.get(myurl,headers=self.agent,verify=False,cert='/search/odin/daemon/pyonsg/utils/ggapi.pem')
		#resp = requests.get(myurl,headers=self.agent,verify=True)
		#print(resp.text)
		#try:
		#	resp = requests.get(myurl)
		#except Exception as e:
		#	pass
		return json.loads(resp.text)
if __name__ == '__main__':
	ggfy = Googlefy()
	result = ggfy.TranslateByGgapi('我爱你','zh','ko')
	#result = ggfy.TranslateByGoogle('我爱你','zh','ko')
	b=result['data']['translations'][0]['translatedText'].encode('utf-8')
	print(b.decode('utf-8'))
	#print(result['data']['translations'][0]['translatedText'])
