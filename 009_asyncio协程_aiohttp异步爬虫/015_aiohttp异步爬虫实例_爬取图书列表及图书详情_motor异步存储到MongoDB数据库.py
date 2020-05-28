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
import aiohttp
import logging

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


# 定义一个通用的爬取方法
semaphore = asyncio.Semaphore(CONCURRENCY)
session = None
async def scrape_api(url):
    # 限制并发请求数量
    async with semaphore:
        try:
            logging.info('scraping %s', url)
            async with session.get(url) as response:
                return await response.json()
        except aiohttp.ClientError:
            logging.error('error occurred while scraping %s', url, exc_info=True)
