# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/26 18:50
Desc:
'''

import asyncio
import requests

# async创建一个协程函数
async def request():
   url = 'https://www.baidu.com'
   status = requests.get(url)
   return status

# 创建一个task的协程列表对象，通用写法
tasks = [asyncio.ensure_future(request()) for _ in range(5)]
print('Tasks:', tasks)

# get_event_loop 方法创建了一个事件循环 loop，
# task对象协程使用wait方法，变成多任务协程，注册到事件循环 loop 中，然后执行协程对象
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

# for循环取出多任务协程执行的结果
for task in tasks:
   print('Task Result:', task.result())