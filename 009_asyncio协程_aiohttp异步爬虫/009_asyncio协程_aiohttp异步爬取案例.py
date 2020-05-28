# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/28 14:53
Desc:
'''
# 导入异步请求库和协程库
import aiohttp
import asyncio

# 看该案例前先查看007和008案例
# async 创建一个协程对象
async def fetch(session, url):
    # with as 语句用于声明一个上下文管理器，能够帮我们自动分配和释放资源，
    # 而在异步方法中，with as 前面加上 async 代表声明一个支持异步的上下文管理器。
    async with session.get(url) as response:
        # 返回响应页面的内容和状态码
        return await response.text(), response.status

async def main():
    # 创建一个异步请求客户端
    async with aiohttp.ClientSession() as session:
        # 调用上面的请求方法
        html, status = await fetch(session, 'https://cuiqingcai.com')
        # 打印出返回的内容，页面内容是字符串，只取前100个
        print(type(html))
        print(f'html: {html[:100]}...')
        print(f'status: {status}')

if __name__ == '__main__':
    '''
    # get_event_loop 方法创建了一个事件循环 loop
    loop = asyncio.get_event_loop()
    # 将上面的main()函数注册到事件循环 loop 中，然后执行协程对象
    loop.run_until_complete(main())
    '''

    # 在 Python 3.7 及以后的版本中，我们可以使用 asyncio.run(main()) 来代替最后的启动操作，
    # 不需要显式声明事件循环，run 方法内部会自动启动一个事件循环。
    # 上面两句代码可以简化为以下代码
    asyncio.run(main())

# 代码解释参考笔记中内容