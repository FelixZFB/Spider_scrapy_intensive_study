# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/31 14:04
Desc:
'''
import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq


async def main():
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto('https://dynamic2.scrape.cuiqingcai.com/')
    await page.waitForSelector('.item .name')
    # 模拟点击
    # 先选定点击的位置，鼠标按钮，点击次数，延迟点击
    await page.click('.item .name', options={
        'button': 'right',
        'clickCount': 1,  # 1 or 2
        'delay': 3000,  # 毫秒
    })
    await browser.close()


# asyncio.get_event_loop().run_until_complete(main())
asyncio.run(main())
