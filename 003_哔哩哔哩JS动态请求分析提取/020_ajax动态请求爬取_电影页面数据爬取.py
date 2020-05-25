# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/25 22:23
Desc:
'''
import requests
import logging
import json
from os import makedirs
from os.path import exists

# 显示调试信息
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

# 电影列表页
INDEX_URL = 'https://dynamic1.scrape.cuiqingcai.com/api/movie/?limit={limit}&offset={offset}'
# 电影详情页面
DETAIL_URL = 'https://dynamic1.scrape.cuiqingcai.com/api/movie/{id}'

# 参数
LIMIT = 10
TOTAL_PAGE = 10
# 存储文件夹名称
RESULTS_DIR = 'results'

# 创建存储文件夹
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)

# 显示调试信息，显示的运行信息
def scrape_api(url):
    logging.info('scraping %s...', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # 直接返回响应结果的json格式数据，返回的实际是一个JsonResponse对象，后面直接可以使用get取出属性对应的值
            return response.json()
        logging.error('get invalid status code %s while scraping %s', response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)

def scrape_index(page):
    # offset的值就是计算得到，第一页就是0，第二页就是10，第三页就是20
    url = INDEX_URL.format(limit=LIMIT, offset=LIMIT * (page - 1))
    return scrape_api(url)

def scrape_detail(id):
    url = DETAIL_URL.format(id=id)
    return scrape_api(url)

def save_data(data):
    # 返回的json数据中取出结果
    name = data.get('name')
    data_path = f'{RESULTS_DIR}/{name}.json'
    '''
    dump 的方法设置了两个参数，一个是 ensure_ascii，我们将其设置为 False，
    它可以保证中文字符在文件中能以正常的中文文本呈现，而不是 unicode 字符；
    另一个是 indent，它的数值为 2，这代表生成的 JSON 数据结果有两个空格缩进，让它的格式显得更加美观
    '''
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


def main():
    for page in range(1, TOTAL_PAGE + 1):
        index_data = scrape_index(page)
        for item in index_data.get('results'):
            id = item.get('id')
            detail_data = scrape_detail(id)
            logging.info('detail data %s', detail_data)
            save_data(detail_data)

if __name__ == '__main__':
    main()