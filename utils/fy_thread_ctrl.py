#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'zhangjingjun'
__mtime__ = '2018/5/23'
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
from pyonsg.utils import baidufy_t
from pyonsg.utils import googlefy_t
from pyonsg.utils import youdaofy_t
from pyonsg.utils import qqfy_t
fromlan='en'
tolan = 'zh'
reqtext='i miss you'

def main():
	threads = []
	# Baidu
	t_bd = baidufy_t.bdThread(target=baidufy_t.getResult_bd, args=(fromlan, tolan, reqtext))
	threads.append(t_bd)
	#google
	t_gg = googlefy_t.ggThread(target=googlefy_t.getResult_gg, args=(fromlan, tolan, reqtext))
	threads.append(t_gg)
	# QQ
	t_qq = qqfy_t.qqThread(target=qqfy_t.getResult_qq, args=(fromlan, tolan, reqtext))
	threads.append(t_qq)
	#youdao
	t_yd = youdaofy_t.ydThread(target=youdaofy_t.getResult_yd, args=(fromlan, tolan, reqtext))
	threads.append(t_yd)

	for thead_id in range(len(threads)):
		threads[thead_id].start()

	print('abcd')
	for thead_id in range(len(threads)):
		threads[thead_id].join()

if __name__ == '__main__':
    main()