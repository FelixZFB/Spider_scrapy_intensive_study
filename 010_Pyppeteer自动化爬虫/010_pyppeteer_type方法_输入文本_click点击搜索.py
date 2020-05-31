# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/31 14:06
Desc:
'''
import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq

width, height = 1366, 768

async def main():
   browser = await launch(headless=False)
   page = await browser.newPage()
   # 设置浏览器窗口大小
   await page.setViewport({'width': width, 'height': height})
   await page.goto('https://www.taobao.com')
   # 输入文本，选定搜索框，然后输入文本
   await page.type('#q', 'iPad')
   # 睡眠5秒
   await asyncio.sleep(5)
   # 点击搜索按钮,会跳转到登陆首页
   # css选择器选择节点：Firefox开发者工具找到页面元素，右键复制 CSS选择器即可
   await page.click('.btn-search', options={
       'button': 'left',
       'clickCount': 1,  # 1 or 2
       'delay': 100,  # 毫秒
   })
   # 睡眠5秒
   await asyncio.sleep(5)

   await browser.close()
 

# asyncio.get_event_loop().run_until_complete(main())
asyncio.run(main())