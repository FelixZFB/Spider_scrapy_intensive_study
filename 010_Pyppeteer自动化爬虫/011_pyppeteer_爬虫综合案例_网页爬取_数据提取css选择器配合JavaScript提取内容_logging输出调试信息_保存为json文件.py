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
# 显示效果如下：
# 2020-06-04 11:21:12,968 - INFO: scraping https://dynamic2.scrape.cuiqingcai.com/page/1
# 2020-06-04 11:21:14,841 - INFO: scraping https://dynamic2.scrape.cuiqingcai.com/detail/ZWYzNCN0ZXVxMGJ0dWEjKC01N3cxcTVvNS0takA5OHh5Z2ltbHlmeHMqLSFpLTAtbWIx
# 2020-06-04 11:21:18,084 - INFO: data {'url': 'https://dynamic2.scrape.cuiqingcai.com/detail/ZWYzNCN0ZXVxMGJ0dWEjKC01N3cxcTVvNS0takA5OHh5Z2ltbHlmeHMqLSFpLTAtbWIx', 'name': '霸王别姬 - Farewell My Concubine', 'categories': ['剧情 ', '爱情 '], 'cover': 'https://p0.meituan.net/movie/ce4da3e03e655b5b88ed31b5cd7896cf62472.jpg@464w_644h_1e_1c', 'score': '9.5', 'drama': '影片借一出《霸王别姬》的京戏，牵扯出三个人之间一段随时代风云变幻的爱恨情仇。段小楼（张丰毅 饰）与程蝶衣（张国荣 饰）是一对打小一起长大的师兄弟，两人一个演生，一个饰旦，一向配合天衣无缝，尤其一出《霸王别姬》，更是誉满京城，为此，两人约定合演一辈子《霸王别姬》。但两人对戏剧与人生关系的理解有本质不同，段小楼深知戏非人生，程蝶衣则是人戏不分。段小楼在认为该成家立业之时迎娶了名妓菊仙（巩俐 饰），致使程蝶衣认定菊仙是可耻的第三者，使段小楼做了叛徒，自此，三人围绕一出《霸王别姬》生出的爱恨情仇战开始随着时代风云的变迁不断升级，终酿成悲剧。'}

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
    # 2020-06-04 11:21:12,968 - INFO: scraping https://dynamic2.scrape.cuiqingcai.com/page/1
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
    # 传入爬取的网址，selector选择器，.item .name选择的是电影名称
    await scrape_page(url, '.item .name')

# querySelectorAllEval 方法，它接收两个参数，
# 第一个参数是 selector，代表要选择的节点对应的 CSS 选择器；
# 第二个参数是 pageFunction，代表的是要执行的 JavaScript 方法，
# 这里需要传入的是一段 JavaScript 字符串，整个方法的作用是选择 selector 对应的节点，
# 然后对这些节点通过 pageFunction 定义的逻辑抽取出对应的结果并返回
# 这里第一个参数 selector 就传入电影名称对应的节点，其实是超链接 a 节点。由于提取结果有多个，所以这里 JavaScript 对应的 pageFunction 输入参数就是 nodes，输出结果是调用了 map 方法得到每个 node，然后调用 node 的 href 属性即可。
# 这样返回结果就是当前列表页的所有电影的详情页 URL 组成的列表了。
async def parse_index():
    return await tab.querySelectorAllEval('.item .name', 'nodes => nodes.map(node => node.href)')

# 传入选择器h2，即等待图书的标题加载出来
async def scrape_detail(url):
    await scrape_page(url, 'h2')

# 根据详情页提取数据
async def parse_detail():
    # 提取标签页的网址
    url = tab.url
    # 选定第一个节点h2，即标题标签，然后执行js代码，提取标签里的文字内容
    name = await tab.querySelectorEval('h2', 'node => node.innerText')
    # 选定所有的.categories button span的节点，调用了 map 方法得到每个 node，然后调用 node 的 href 属性即可，返回的结果是要一个列表
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


# 上面返回数据是字典格式，然后使用dump方法存储为json格式
async def save_data(data):
    name = data.get('name')
    data_path = f'{RESULTS_DIR}/{name}.json'
    # 指定编码，ensure_ascii=False支持中文，防止乱码出现
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


async def main():
    await init()
    try:
        # 遍历爬取每一个列表页面
        for page in range(1, TOTAL_PAGE + 1):
            # 爬取网页，返回加载后的网页内容
            await scrape_index(page)
            # 提取列表页所有的网址，返回一个URL列表
            detail_urls = await parse_index()
            # 然后遍历每个网址，去爬取详细内容
            for detail_url in detail_urls:
                # 爬取加载详细内容
                await scrape_detail(detail_url)
                # 提取详细内容，返回结果
                detail_data = await parse_detail()
                logging.info('data %s', detail_data)
                # 保存数据
                await save_data(detail_data)
    # 关闭浏览器
    finally:
        await browser.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
