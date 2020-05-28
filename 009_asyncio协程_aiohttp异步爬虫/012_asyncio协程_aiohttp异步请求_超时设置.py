# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/28 21:05
Desc:
'''

import asyncio
import aiohttp

# 创建协程函数
async def main():
    # 设置超时参数，超时时间1秒
    timeout = aiohttp.ClientTimeout(total=1)
    # 创建aiohttp异步请求客户端
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # 使用客户端发送post请求，使用with as，前面加上async支持异步的上下文管理器
        async with session.get('https://httpbin.org/get') as response:
            print('status:', response.status)

if __name__ == '__main__':
    # asyncio.get_event_loop().run_until_complete(main())
    # 上面代码使用以下简写
    asyncio.run(main())

# 其类型为 asyncio.TimeoutError，我们再进行异常捕获即可。
