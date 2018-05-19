#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'zhangjingjun'
__mtime__ = '2018/5/16'
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
import random
import hashlib
import urllib
import requests
import json

class Youdaofy:
	def __init__(self):
		self.appKey = "6ae9815f6d6129db"
		self.sec_key = "3DfMT6NVupkamXtBu2z5BF4rVAMMA9YC"
		self.salt = random.randint(10000, 99999)


	def sign(self,query):
		hl = hashlib.md5()
		sign_str = self.appKey + query + str(self.salt) + self.sec_key
		hl.update(sign_str.encode(encoding='utf-8'))
		x = hl.hexdigest()
		return x


	def getResult(self,fromlang,tolang,query):
		signid = self.sign(query)
		myurl = 'http://openapi.youdao.com/api'+'?appKey='+ self.appKey+'&q='+urllib.parse.quote(query)+'&from='+fromlang+'&to='+tolang+'&salt='+str(self.salt)+'&sign='+signid
		try:
			resp = requests.get(myurl)
		except Exception as e:
			pass
		#print(resp.text)
		return json.loads(resp.text)



if __name__ == '__main__':
	bdfy = Youdaofy()
	result = bdfy.getResult('zh','en','我爱你')
	print(result['translation'])
	#print(result['trans_result'][0]['dst'])


