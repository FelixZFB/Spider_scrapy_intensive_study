# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/31 13:20
Desc:
'''
import asyncio
from pyppeteer import launch


async def main():
    browser = await launch(headless=False)

    # 新建页面1
    page = await browser.newPage()
    await page.goto('https://www.baidu.com')

    # 新建页面2
    page = await browser.newPage()
    await page.goto('https://www.bing.com')

    # 返回当前所有页面
    pages = await browser.pages()
    print('Pages:', pages)

    # 选择页面1
    page1 = pages[1]
    # 切换进入页面1
    await page1.bringToFront()
    await asyncio.sleep(10)

    await browser.close()


# asyncio.get_event_loop().run_until_complete(main())
asyncio.run(main())