# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/28 16:20
Desc:
'''
import aiohttp
import asyncio

# 定义一个协程主函数
async def main():
    # 请求时候携带的参数
    data = {'name': 'germey', 'age': 25}
    # 创建一个aiohttp的客户端
    async with aiohttp.ClientSession() as session:
        # 使用客户端发送post请求，使用with as，前面加上async支持异步的上下文管理器
        async with session.post('https://httpbin.org/post', data=data) as response:
            # 返回响应的各个字段
            print('status:', response.status)
            print('headers:', response.headers)
            print('body:', await response.text())
            print('bytes:', await response.read())
            print('json:', await response.json())
            # 有些字段前面需要加 await，有的则不需要。状态码是数字就不需要。
            # 其原则是，如果其返回的是一个 coroutine 对象（如 async 修饰的方法），那么前面就要加 await

if __name__ == '__main__':
    # asyncio.get_event_loop().run_until_complete(main())
    # 上面代码使用以下简写
    asyncio.run(main())
