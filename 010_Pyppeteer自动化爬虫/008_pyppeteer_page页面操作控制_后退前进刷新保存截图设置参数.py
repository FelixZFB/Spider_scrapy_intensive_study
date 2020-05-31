# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/31 13:26
Desc:
'''

import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq


async def main():
    browser = await launch(headless=False)
    page = await browser.newPage()
    # 先访问一个网页
    await page.goto('https://dynamic1.scrape.cuiqingcai.com/')
    await asyncio.sleep(2)
    # 等待2秒后访问另外一个网页
    await page.goto('https://dynamic2.scrape.cuiqingcai.com/')
    # 后退
    await page.goBack()
    await asyncio.sleep(2)
    # 前进
    await page.goForward()
    await asyncio.sleep(2)
    # 刷新
    await page.reload()
    await asyncio.sleep(2)
    # 保存 PDF
    # await page.pdf()
    # 截图
    await page.screenshot(path='example1.png')
    await asyncio.sleep(2)
    # 设置页面 HTML
    await page.setContent('<h2>Hello World</h2>')
    # 设置 User-Agent
    await page.setUserAgent('Python')
    # 设置 Headers
    await page.setExtraHTTPHeaders(headers={})
    # 关闭
    await page.close()
    await browser.close()


# asyncio.get_event_loop().run_until_complete(main())
asyncio.run(main())