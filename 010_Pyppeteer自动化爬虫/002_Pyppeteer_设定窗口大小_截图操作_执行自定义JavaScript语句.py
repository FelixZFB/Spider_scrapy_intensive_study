# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/31 11:23
Desc:
'''

import asyncio
from pyppeteer import launch

width, height = 1366, 768

# 定义协程函数
async def main():
    # 创建浏览器对象，新建页面
    browser = await launch(headless=False)
    page = await browser.newPage()
    # 设置浏览器窗口大小
    await page.setViewport({'width': width, 'height': height})
    # 请求网页
    await page.goto('https://dynamic2.scrape.cuiqingcai.com/')
    # 解析返回内容
    await page.waitForSelector('.item .name')
    await asyncio.sleep(2)
    # 网页截图，然后保存
    await page.screenshot(path='example.png')
    # evaluate 方法执行了一些 JavaScript，JavaScript 传入的是一个函数
    # 里面传入的是JavaScript代码，使用 return 方法返回了网页的宽高、像素大小比率三个值，最后得到的是一个 JSON 格式的对象
    dimensions = await page.evaluate('''() => {
       return {
           width: document.documentElement.clientWidth,
           height: document.documentElement.clientHeight,
           deviceScaleFactor: window.devicePixelRatio,
       }
   }''')

    print(dimensions)
    await browser.close()


# 创建loop循环，加入并启动函数
# asyncio.get_event_loop().run_until_complete(main())
# 上面代码使用以下简写
asyncio.run(main())
