# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/29 16:27
Desc:
'''
import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq

# async关键字定义协程方法
async def main():
    # 创建await关键字创建一个客户端对象，支持异步，遇到await关键字可以挂起当前操作，继续下一步操作
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://dynamic2.scrape.cuiqingcai.com/')
    await page.waitForSelector('.item .name')
    doc = pq(await page.content())
    names = [item.text() for item in doc('.item .name').items()]
    print('Names:', names)
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
