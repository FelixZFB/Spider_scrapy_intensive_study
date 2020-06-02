# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/31 14:31
Desc:
'''
import logging
from os.path import exists
from os import makedirs
import json
import asyncio
from pyppeteer import launch
from pyppeteer.errors import TimeoutError

# 调试输出信息，调试输出级别，格式
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

# 基本配置，网址
INDEX_URL = 'https://dynamic2.scrape.cuiqingcai.com/page/{page}'
TIMEOUT = 10
TOTAL_PAGE = 10
RESULTS_DIR = 'results'

# 浏览器窗口
WINDOW_WIDTH, WINDOW_HEIGHT = 1366, 768

# 判断是否有文件夹没有就创建
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)

# 定义浏览器，窗口名称
browser, tab = None, None
# 无头模式，设置False就会打开浏览器操作
HEADLESS = True


# 初始化方法，定义浏览器和窗口对象，设置窗口大小
async def init():
    # 将浏览器和窗口定义为全局变量
    global browser, tab
    # await 关键字修饰创建支持协程并发操作的浏览器对象，参考001案例参数说明，f格式化字符串设置窗口尺寸
    browser = await launch(headless=HEADLESS,
                           args=['--disable-infobars', f'--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}'])
    # await 关键字修饰创建浏览器页面对象
    tab = await browser.newPage()
    # 设置窗口大小
    await tab.setViewport({'width': WINDOW_WIDTH, 'height': WINDOW_HEIGHT})


# 定义一个通用的爬取页面方法
async def scrape_page(url, selector):
    # 显示正在爬取网址信息
    logging.info('scraping %s', url)
    try:
        # 请求网址，等待页面加载符合selector节点要获取的内容，加载出页面
        await tab.goto(url)
        await tab.waitForSelector(selector, options={
            'timeout': TIMEOUT * 1000   # 设置等待超时时间，超时进行下面报错
        })
    except TimeoutError:
        logging.error('error occurred while scraping %s', url, exc_info=True)


# 爬取列表页的方法，传入页码，得到爬取的url
async def scrape_index(page):
    # INDEX_URL = 'https://dynamic2.scrape.cuiqingcai.com/page/{page}'
    url = INDEX_URL.format(page=page)
    await scrape_page(url, '.item .name')


async def parse_index():
    return await tab.querySelectorAllEval('.item .name', 'nodes => nodes.map(node => node.href)')


async def scrape_detail(url):
    await scrape_page(url, 'h2')


async def parse_detail():
    url = tab.url
    name = await tab.querySelectorEval('h2', 'node => node.innerText')
    categories = await tab.querySelectorAllEval('.categories button span', 'nodes => nodes.map(node => node.innerText)')
    cover = await tab.querySelectorEval('.cover', 'node => node.src')
    score = await tab.querySelectorEval('.score', 'node => node.innerText')
    drama = await tab.querySelectorEval('.drama p', 'node => node.innerText')
    return {
        'url': url,
        'name': name,
        'categories': categories,
        'cover': cover,
        'score': score,
        'drama': drama
    }


async def save_data(data):
    name = data.get('name')
    data_path = f'{RESULTS_DIR}/{name}.json'
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


async def main():
    await init()
    try:
        for page in range(1, TOTAL_PAGE + 1):
            await scrape_index(page)
            detail_urls = await parse_index()
            for detail_url in detail_urls:
                await scrape_detail(detail_url)
                detail_data = await parse_detail()
                logging.info('data %s', detail_data)
                await save_data(detail_data)
    finally:
        await browser.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
