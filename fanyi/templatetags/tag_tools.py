#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'zhangjingjun'
__mtime__ = '2018/3/29'
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
from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag
def formatTime(intime):
	return intime.strftime("%m%d %H:%M")

@register.simple_tag
def formatIp(inip):
	ip = 'http://10.153.51.60:12000/xml'
	ip_list = inip.split('/')
	# print(ip_list)
	return ip_list[2]


if __name__ == '__main__':
	pass
