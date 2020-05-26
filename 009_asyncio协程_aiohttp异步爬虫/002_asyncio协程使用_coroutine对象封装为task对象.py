# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/26 17:09
Desc:
'''
import asyncio

# 使用async关键字定义一个协程函数，该函数调用时候不会直接执行，而是返回一个协程对象
async def execute(x):
   print('Number:', x)
   return x

# 调用协程方法，传入参数，返回了一个 coroutine 协程对象
coroutine = execute(1)
print('Coroutine:', coroutine)
print('After calling execute')

# get_event_loop 方法创建了一个事件循环 loop，
loop = asyncio.get_event_loop()

# 继续将coroutine 协程对象封装进task对象
task = loop.create_task(coroutine)
print('Task对象状态:', task)

# 并调用了 loop 对象的 run_until_complete 方法将task对象协程注册到事件循环 loop 中，然后启动执行
loop.run_until_complete(task)
print('Task对象状态:', task)
print('After calling loop')

# 将 coroutine 对象转化为了 task 对象，随后我们打印输出一下，发现它是 pending 状态。
# 接着我们将 task 对象添加到事件循环中得到执行，随后我们再打印输出一下 task 对象，
# 发现它的状态就变成了 finished