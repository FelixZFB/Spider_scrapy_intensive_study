# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/26 18:59
Desc:
'''
import asyncio
import requests
import time
 
start = time.time()

# #async创建一个协程函数
async def request():
   url = 'https://static4.scrape.cuiqingcai.com/'
   print('Waiting for', url)
   response = requests.get(url)
   print('Get response from', url, 'response', response)
 
# 创建一个task的协程列表对象，通用写法
tasks = [asyncio.ensure_future(request()) for _ in range(10)]
# get_event_loop 方法创建了一个事件循环 loop，
loop = asyncio.get_event_loop()
# task对象协程使用wait方法，变成多任务协程，注册到事件循环 loop 中，然后执行协程对象
loop.run_until_complete(asyncio.wait(tasks))
 
end = time.time()
print('Cost time:', end - start)

# 运行发现
# 发现和正常的请求并没有什么两样，依然还是顺次执行的，一个请求完了，在开始下一次请求，耗时 51 秒，
# 平均一个请求耗时 5 秒，说好的异步处理,参考006案例