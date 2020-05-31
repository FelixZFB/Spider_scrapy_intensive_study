# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/31 12:57
Desc:
'''
import asyncio
from pyppeteer import launch

width, height = 1920, 980

async def main():
    # 创建浏览器对象，和浏览器页面对象
    # userdata 属性用于保存浏览器一些配置信息，用户登录信息，Cache、Cookies 等各种信息，避免每次都重新登录
    browser = await launch(headless=False, args=['--disable-infobars'], userDataDir='./userdata')
    page = await browser.newPage()
    # 设置浏览器窗口大小
    await page.setViewport({'width': width, 'height': height})
    #  evaluateOnNewDocument，意思就是在每次加载网页的时候执行某个语句，所以这里我们可以执行一下将 WebDriver 隐藏的命令
    # navigator的webdriver属性隐藏后，就可以避过浏览器自动化工具检测
    await page.evaluateOnNewDocument('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')
    await page.goto('https://antispider1.scrape.cuiqingcai.com/')
    await asyncio.sleep(10)


# 创建loop循环，加入并启动函数
# asyncio.get_event_loop().run_until_complete(main())
# 上面代码使用以下简写
asyncio.run(main())
