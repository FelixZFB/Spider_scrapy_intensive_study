# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/26 16:21
Desc:
'''
# 导入协程库
import asyncio

# 使用async关键字定义一个协程函数，该函数调用时候不会直接执行，而是返回一个协程对象
async def execute(x):
   print('Number:', x)

# 调用协程方法，传入参数，返回了一个 coroutine 协程对象
coroutine = execute(1)
print('Coroutine协程对象:', coroutine)
print('协程对象注册到loop循环中')

# get_event_loop 方法创建了一个事件循环 loop，
loop = asyncio.get_event_loop()
# 并调用了 loop 对象的 run_until_complete 方法将协程注册到事件循环 loop 中，然后启动执行
print('执行loop循环中的函数')
loop.run_until_complete(coroutine)
print('After calling loop')

# coroutine 对象传递给 run_until_complete 方法的时候，
# 实际上它进行了一个操作就是将 coroutine 封装成了 task 对象