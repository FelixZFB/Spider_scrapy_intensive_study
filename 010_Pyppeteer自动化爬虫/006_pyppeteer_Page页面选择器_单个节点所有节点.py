# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/31 13:14
Desc:
'''
import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq


async def main():
    # 新建浏览器和页面对象
    browser = await launch()
    page = await browser.newPage()
    # 请求网页
    await page.goto('https://dynamic2.scrape.cuiqingcai.com/')
    # 选择节点
    await page.waitForSelector('.item .name')

    # 返回第一个节点，以下两种方式结果一样
    j_result1 = await page.J('.item .name')
    j_result2 = await page.querySelector('.item .name')

    # 返回所有的节点，以下两种方式结果一样
    jj_result1 = await page.JJ('.item .name')
    jj_result2 = await page.querySelectorAll('.item .name')
    print('J Result1:', j_result1)
    print('J Result2:', j_result2)
    print('JJ Result1:', jj_result1)
    print('JJ Result2:', jj_result2)

    await browser.close()


# asyncio.get_event_loop().run_until_complete(main())
asyncio.run(main())
