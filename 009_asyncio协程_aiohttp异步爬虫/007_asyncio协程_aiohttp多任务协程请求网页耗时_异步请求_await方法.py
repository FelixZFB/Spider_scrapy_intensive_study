# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/26 22:10
Desc:
'''
import asyncio
import requests
import time
import aiohttp

start = time.time()

# async创建一个协程函数，即一个原生 coroutine 协程对象， 用于 request 函数中 await 后面接的参数
async def get(url):
    # 创建一个客户端
    session = aiohttp.ClientSession()
    # 使用ClientSession类实例的get方法发送请求
    response = await session.get(url)
    await session.close()
    return response

# async创建一个协程函数
async def request():
    url = 'https://www.baidu.com/'
    print('Waiting for', url)
    response = await get(url)
    print('Get response from', url, 'response', response)


# 创建一个task的协程列表对象，通用写法
tasks = [asyncio.ensure_future(request()) for _ in range(100)]
# get_event_loop 方法创建了一个事件循环 loop，
loop = asyncio.get_event_loop()
# task对象协程使用wait方法，变成多任务协程，注册到事件循环 loop 中，然后执行协程对象
loop.run_until_complete(asyncio.wait(tasks))

end = time.time()
print('Cost time:', end - start)

# 运行发现
# 耗时只有0.92秒，相比006案例提升巨大