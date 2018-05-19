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
import requests
import urllib
import random
import time
import hmac
import hashlib
import base64
import json

class Qqfy:
	def __init__(self):
		self.sec_id = "AKIDSuCMMC3cLyQgkfSgkMLHB1oCbw9Iqpz9"
		self.sec_key = 'IWbVGqFUYZZZVHsHWecXN4a5WqzxmQuD'
		self.salt = random.randint(10000, 99999)
		self.Timestamp = int(time.time())

	def buildSign(self,**req_dict):
		reqstr=''
		#sec_key='Gu5t9xGARNpq86cd98joQYCN3EXAMPLE'
		for key in req_dict:
			reqstr+=(key+'='+str(req_dict[key])+'&')
		reqstr=(reqstr[0:-1])
		srcstr='GETtmt.tencentcloudapi.com/?'+reqstr
		#srcstr='GETcvm.tencentcloudapi.com/?Action=DescribeInstances&InstanceIds.0=ins-09dx96dg&Limit=20&Nonce=11886&Offset=0&Region=ap-guangzhou&SecretId=AKIDz8krbsJ5yKBZQpn74WFkmLPx3EXAMPLE&Timestamp=1465185768&Version=2017-03-12'
		h = hmac.new(bytes(self.sec_key,'utf-8'), bytes(srcstr,'utf-8'), hashlib.sha1).digest()
		signStr = base64.b64encode(h)
		return signStr.decode('utf-8')

	def TranslateByQQ(self, fromLang, text, toLang):
		req_dict={
			'Action': 'TextTranslate',
			'Nonce': self.salt,
			'ProjectId':0,
			'Region': 'ap-beijing',
			'SecretId':self.sec_id,
			'Source': fromLang,
			'SourceText': text,
			'Target': toLang,
			'Timestamp':self.Timestamp,
			'Version':'2018-03-21'
		}
		req_dict['Signature']=self.buildSign(**req_dict)
		urlstr=""
		for key in req_dict:
			urlstr+=(key+'='+urllib.parse.quote(str(req_dict[key]))+'&')
		urlstr=urlstr[0:-1]
		sufix='https://tmt.tencentcloudapi.com/?'
		#sufix='GETtmt.api.qcloud.com/v2/index.php?'
		print(sufix+urlstr)
		resp = requests.get(sufix+urlstr)
		return json.loads(resp.text)


if __name__ == '__main__':
	qqfy = Qqfy()
	result = qqfy.TranslateByQQ('zh','吃饭','ru')
	print(result)
	print(result['Response']['TargetText'])