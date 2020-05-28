# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/28 21:13
Desc:
'''
import asyncio
import aiohttp

# 定义基本参数，并发数量限制
CONCURRENCY = 5
URL = 'https://www.baidu.com'
# Semaphore 创建了一个信号量对象，赋值为 semaphore，控制并发量
semaphore = asyncio.Semaphore(CONCURRENCY)


# 创建发送请求的协程函数
async def scrape_api(session):
    # 使用 async with 语句将 semaphore 作为上下文对象即可，就可以控制并发量
    # 信号量可以控制进入爬取的最大协程数量，最大数量就是我们声明的 CONCURRENCY 的值。
    async with semaphore:
        print('scraping', URL)
        # 使用session客户端发送get请求，使用with as，前面加上async支持异步的上下文管理器
        async with session.get(URL) as response:
            # 等待2秒后，返回结果，然后进行下一次并发请求
            await asyncio.sleep(2)
            print(response.status)
            await asyncio.sleep(2)
            return await response.text()

# 创建协程主函数
async def main():
    # 创建aiohttp异步请求客户端
    session = aiohttp.ClientSession()
    # 使用ensure_future方法创建大量并发请求的任务列表
    scrape_index_tasks = [asyncio.ensure_future(scrape_api(session)) for _ in range(10000)]
    # 任务列表传递给 gather 方法运行，每次只会运行5个
    # 008案例中并发请求使用的是wait方法，此处需要进行限制，使用gather方法
    await asyncio.gather(*scrape_index_tasks)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    # 上面代码使用以下简写，此处使用以下简写会报错，需要注册同一个循环，只能使用上面写法
    # asyncio.run(main())