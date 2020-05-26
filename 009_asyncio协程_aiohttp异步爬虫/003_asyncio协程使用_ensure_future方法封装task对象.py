# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/26 17:19
Desc:
'''
import asyncio
async def execute(x):
   print('Number:', x)
   return x
coroutine = execute(1)
print('Coroutine:', coroutine)
print('After calling execute')

# syncio 的 ensure_future 方法，返回结果也是 task 对象，这样的话我们就可以不借助于 loop 来定义，
# 即使我们还没有声明 loop 也可以提前定义好 task 对象
# 和002案例对比，输出结果一样，只是不通过loop.create_task来定义task对象
task = asyncio.ensure_future(coroutine)
print('Task:', task)

# get_event_loop 方法创建了一个事件循环 loop，
loop = asyncio.get_event_loop()
# 执行任务
loop.run_until_complete(task)
print('Task:', task)
print('After calling loop')