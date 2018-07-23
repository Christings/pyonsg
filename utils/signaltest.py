#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'zhangjingjun'
__mtime__ = '2018/5/26'
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
import xml.etree.ElementTree as ET
import requests
import urllib
import time
from threading import Thread

#继承和重写线程，支持返回结果获取
class newThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return

#带返回值get请求
def getResult(http_url,query):
    ret = {'status': True, 'error': None, 'data': None,'cost':None}
    req_url = http_url + '?key='+urllib.parse.quote(query)
    try:
        start_time = int(time.time()*1000)
        resp = requests.get(req_url)
        end_time = int(time.time()*1000)
        result = parseXml(resp.text)
    except Exception as e:
        ret['status'] = False
        ret['error'] = 'Error:'+str(e)
        return 1
    ret['cost'] = end_time - start_time
    if result['status'] == True:
        ret['data'] = result['data']
    else:
        ret['status'] = False
        ret['error'] = result['error']
    return ret

#解析xml结果
def parseXml(xml_str):
    ret = {'status':True,'error':None,'data':None}
    try:
        root=ET.fromstring(xml_str)
    except Exception as e:
        ret['status']=False
        ret['error']='Error:'+str(e)
    ret['data']= root[1][2].text
    return ret


if __name__ == '__main__':
    url_first = 'http://127.0.0.1:8000/test_xml'
    url_second = 'http://127.0.0.1:8000/test_xml'
    query = '你好'
    threads = []
    try:
        req_first = newThread(target=getResult, args=(url_first, query))
        threads.append(req_first)
        req_second = newThread(target=getResult, args=(url_first, query))
        threads.append(req_second)
        for sub_thead in threads:
            sub_thead.start()
        result_first = threads[0].join()
        result_second = threads[1].join()
        if result_first['status'] == True and result_first['status'] == True:
            print("result", result_first['data'], ' cost', result_first['cost'])
            print("result", result_second['data'], ' cost', result_second['cost'])
        else:
            print('request error'+req_first['error']+req_second['error'])
    except Exception as e:
        print(e)