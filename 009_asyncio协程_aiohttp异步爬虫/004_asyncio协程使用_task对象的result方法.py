# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/26 18:33
Desc:
'''
import asyncio
import requests

# 定义一个请求方法
async def request():
   url = 'https://www.baidu.com'
   response = requests.get(url)
   print(response)
   return response

# 封装一个task协程对象
coroutine = request()
task = asyncio.ensure_future(coroutine)
print('Task:', task)

# get_event_loop 方法创建了一个事件循环 loop，
# task对象协程注册到事件循环 loop 中，执行协程对象
loop = asyncio.get_event_loop()
loop.run_until_complete(task)
print('Task:', task)

# 返回任务执行的结果
print('Task Result:', task.result())