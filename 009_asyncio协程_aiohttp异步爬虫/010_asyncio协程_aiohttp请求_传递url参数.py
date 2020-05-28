# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/28 16:13
Desc:
'''
import aiohttp
import asyncio

async def main():
    # url参数使用一个字典传递进去
    params = {'name': 'germey', 'age': 25}
    # 创建一个aiohttp的客户端，用于发送请求
    async with aiohttp.ClientSession() as session:
        # 传递参数给url
        # 实际请求的url是：https://httpbin.org/get?name=germey&age=25
        async with session.get('https://httpbin.org/get', params=params) as response:
            print(await response.text())

if __name__ == '__main__':
    # asyncio.get_event_loop().run_until_complete(main())
    # 上面代码使用以下简写
    asyncio.run(main())