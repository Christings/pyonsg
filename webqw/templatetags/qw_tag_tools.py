#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'zhangjingjun'
__mtime__ = '2018/4/12'
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
def formatStr(instr):
	print(instr)
	#newstr=instr.replace('\n','\r\n')
	newstr = instr.split('\n')
	print(newstr)
	return len(newstr)


@register.simple_tag
def formatStr2(instr):
	print(instr)
	newstr=instr.replace('\n','\r\n')
	#newstr = instr.split('\n')
	print(newstr)
	return newstr



if __name__ == '__main__':
	pass