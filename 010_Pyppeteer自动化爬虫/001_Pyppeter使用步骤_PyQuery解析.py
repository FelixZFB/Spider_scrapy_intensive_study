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
    # 1.launch 方法会新建一个 Browser 对象，最终会得到一个 Browser 对象，然后赋值给 browser。这一步就相当于启动了浏览器。
    # 创建await关键字创建一个客户端对象，支持异步，遇到await关键字可以挂起当前操作，继续下一步操作
    # launch()实际是一个 async 修饰的方法(原生协程对象)，所以调用它的时候需要使用 await
    # browser = await launch()
    # 常用参数设置，也可以写成 headless=False，也可以写成下面字典形式
    browser = await launch({
        'headless': False,
        # 'executablePath': '‪H:\ProgramDevelop\chrome-win\chrome.exe' # 由于版本兼容性问题，报错
        'devtools': True, # 启动调试模式，浏览器会显示调试窗口
        'args': ['--disable-infobars'], # 去掉 Chrome 正受到自动测试软件的控制

    })

    # 2.browser 调用 newPage  方法相当于浏览器中新建了一个选项卡，同时新建了一个 Page 对象，这时候新启动了一个选项卡，但是还未访问任何页面，浏览器依然是空白。
    page = await browser.newPage()

    # 3.Page 对象调用了 goto 方法就相当于在浏览器中输入了这个 URL，浏览器跳转到了对应的页面进行加载。
    await page.goto('https://dynamic2.scrape.cuiqingcai.com/')

    # 4.Page 对象调用 waitForSelector 方法，传入选择器selector，使用css选择器语法，
    # 获取要选择器内容，那么页面就会等待选择器所对应的节点信息加载出来，如果加载出来了，立即返回，否则会持续等待直到超时。此时如果顺利的话，页面会成功加载出来。
    await page.waitForSelector('.item .name')

    # 5.页面加载完成之后再调用 content 方法，可以获得当前浏览器页面的源代码(浏览器JavaScript动态渲染以后的页面元素的代码，开发者工具查看元素里面的代码，并不是右键查看源代码中的代码)，这就是 JavaScript 渲染后的结果。
    # 同时将返回的动态渲染后的网页源代码返回成一个pyquery对象
    doc = pq(await page.content())

    # 6.pyquery 进行使用css选择器解析并提取页面的电影名称，就得到最终结果了
    names = [item.text() for item in doc('.item .name').items()]
    print('Names:', names)

    # 7.关闭浏览器对象
    await browser.close()


# 创建loop循环，加入并启动函数
# asyncio.get_event_loop().run_until_complete(main())
# 上面代码使用以下简写
asyncio.run(main())
