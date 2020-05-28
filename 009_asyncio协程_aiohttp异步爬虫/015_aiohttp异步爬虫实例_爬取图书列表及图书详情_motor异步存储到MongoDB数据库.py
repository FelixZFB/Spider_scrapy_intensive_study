# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/28 22:22
Desc:
'''
import asyncio
import json
import time

import aiohttp
import logging

from aiohttp import ContentTypeError
from motor.motor_asyncio import AsyncIOMotorClient

# 设置调试logging基本配置
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')
# 列表页及详情页网址
INDEX_URL = 'https://dynamic5.scrape.cuiqingcai.com/api/book/?limit=18&offset={offset}'
DETAIL_URL = 'https://dynamic5.scrape.cuiqingcai.com/api/book/{id}'
# 一页显示的图书数量，总页码数
PAGE_SIZE = 18
PAGE_NUMBER = 100
# 并发限制数量
CONCURRENCY = 5

# MongoDB数据库基本信息
MONGO_CONNECTION_STRING = 'mongodb://localhost:27017'
MONGO_DB_NAME = 'cui_books'
MONGO_COLLECTION_NAME = 'cui_books'

# motor异步存储连接MongoDB数据库
client = AsyncIOMotorClient(MONGO_CONNECTION_STRING)
db = client[MONGO_DB_NAME]
collection = db[MONGO_CONNECTION_STRING]

# get_event_loop 方法创建了一个事件循环 loop，用于注册执行任务列表
loop = asyncio.get_event_loop()

class Spider(object):

    def __init__(self):
        # Semaphore 创建了一个信号量对象，赋值为 semaphore，控制并发量
        self.semaphore = asyncio.Semaphore(CONCURRENCY)

    # 创建一个通用的爬虫协程方法
    async def scrape_api(self, url):
        # 使用 async with 语句将 semaphore 作为上下文对象即可，就可以控制并发量
        # 信号量可以控制进入爬取的最大协程数量，最大数量就是我们声明的 CONCURRENCY 的值。
        async with self.semaphore:
            try:
                logging.info('scraping %s', url)
                # 使用session客户端发送get请求，使用with as，前面加上async支持异步的上下文管理器
                async with self.session.get(url) as response:
                    # 每次并发请求5个网址，然后睡眠1秒后，进行下步操作，减小服务器压力
                    await asyncio.sleep(1)
                    # 返回响应的json数据，json()方法返回的就是python的字典数据
                    return await response.json()
            # 捕获类型错误
            except ContentTypeError as e:
                logging.error('error occurred while scraping %s', url, exc_info=True)

    # 抓取列表页
    async def scrape_index(self, page):
        # 根据页码构造url地址
        url = INDEX_URL.format(offset=PAGE_SIZE * (page - 1))
        # 调用的 async 修饰的scrape_api 方法前面需要加 await
        return await self.scrape_api(url)

    # 抓取详情页面数据
    async def scrape_detail(self, id):
        # 根据图书id构造url地址
        url = DETAIL_URL.format(id=id)
        # 获取json数据，调用的 async 修饰的scrape_api 方法前面需要加 await
        data = await self.scrape_api(url)
        # 处理保存数据，上面请求之后的response的json()方法返回的就是python的字典数据
        await self.save_data(data)

    # 图书信息异步存储到MongoDB的方法
    async def save_data(self, data):
        logging.info('saving data %s', data)
        # 如果数据存在
        if data:
            # 存储数据，更新加入一条数据
            return await collection.update_one({
                'id': data.get('id')
            }, {
                '$set': data
            }, upsert=True)

    # 主函数
    async def main(self):
        # 创建一个aiohttp异步请求的客户端
        self.session = aiohttp.ClientSession()

        # 列表页任务列表，ensure_future创建一个task的协程列表对象
        scrape_index_tasks = [asyncio.ensure_future(self.scrape_index(page)) for page in range(1, PAGE_NUMBER + 1)]
        # 并发执行任务返回结果，上面任务列表传递给 gather 方法启动运行，每次只会运行5个
        # 调用将结果赋值为results，它是所有task返回结果组成的列表
        results = await asyncio.gather(*scrape_index_tasks)

        # 详情页任务列表
        print('results', results)
        ids = []
        # 先获取所有图书的从上面每页结果中取出每本图书的id
        for index_data in results:
            # 如果results列表中有数据，if not True继续向下执行后面的语句，
            # 如果没有数据了，if not False就执行continue，忽略后面语句，跳出当前的循环
            if not index_data:
                continue
            for item in index_data.get('results'):
                ids.append(item.get('id'))
        # 图形详情的任务列表，ensure_future创建一个task的协程列表对象
        scrape_detail_tasks = [asyncio.ensure_future(self.scrape_detail(id)) for id in ids]
        # gather 方法启动并发运行
        await asyncio.wait(scrape_detail_tasks)
        # 最后所有执行完毕关闭客户端
        await self.session.close()


if __name__ == '__main__':
    spider = Spider()
    loop.run_until_complete(spider.main())
