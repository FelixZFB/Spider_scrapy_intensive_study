# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/26 22:46
Desc:
'''
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


def test(number):
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
        # print('Waiting for', url)
        # response = await get(url)
        await get(url)
        # print('Get response from', url, 'response', response)


    # 创建一个task的协程列表对象，通用写法
    tasks = [asyncio.ensure_future(request()) for _ in range(number)]
    # get_event_loop 方法创建了一个事件循环 loop，
    loop = asyncio.get_event_loop()
    # task对象协程使用wait方法，变成多任务协程，注册到事件循环 loop 中，然后执行协程对象
    loop.run_until_complete(asyncio.wait(tasks))

    end = time.time()
    print('Number:', number, 'Cost time:', end - start)


for num in [10, 30, 50, 100, 500]:
    test(num)

# 即使我们增加了并发数量，但在服务器能承受高并发的前提下，其爬取速度几乎不太受影响。
# 使用了异步请求之后，我们几乎可以在相同的时间内实现成百上千倍次的网络请求，
# 把这个运用在爬虫中，速度提升是非常可观的。