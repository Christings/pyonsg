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

class Badufy:
	def __init__(self):
		self.appid = "20180516000160525"
		self.sec_key = "4QoUOqERE4Mx_dD2S_MQ"
		self.salt = random.randint(10000, 99999)


	def sign(self,query):
		hl = hashlib.md5()
		sign_str = self.appid + query + str(self.salt) + self.sec_key
		hl.update(sign_str.encode(encoding='utf-8'))
		x = hl.hexdigest()
		return x


	def getResult(self,fromlang,tolang,query):
		signid = self.sign(query)
		myurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'+'?appid='+ self.appid+'&q='+urllib.parse.quote(query)+'&from='+fromlang+'&to='+tolang+'&salt='+str(self.salt)+'&sign='+signid
		try:
			resp = requests.get(myurl)
		except Exception as e:
			pass
		return json.loads(resp.text)



if __name__ == '__main__':
	bdfy = Badufy()
	result = bdfy.getResult('zh','ara','我想你')
	print(result['trans_result'][0]['dst'])


