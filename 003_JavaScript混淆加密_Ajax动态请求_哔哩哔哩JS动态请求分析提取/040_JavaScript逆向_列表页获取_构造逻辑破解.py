# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/7/23 10:23
Desc:
'''
import hashlib
import time
import base64
from typing import List, Any
import requests

# 列表页构造地址
INDEX_URL = 'https://dynamic6.scrape.cuiqingcai.com/api/movie?limit={limit}&offset={offset}&token={token}'
# 详情页构造地址
DETAIL_URL = 'https://dynamic6.scrape.cuiqingcai.com/api/movie/{id}?token={token}'
# 列表页电影数量，第一页offset为0
LIMIT = 10
OFFSET = 0
# 一个固定的字符串，用于和电影ID拼接后构造加密后的电影ID
SECRET = 'ef34#teuq0btua#(-57w1q5o5--j@98xygimlyfxs*-!i-0-mb'


# token 参数逆向获取，指定传入参数类型是一个列表
def get_token(args: List[Any]):
    # 获取当前时间戳
    timestamp = str(int(time.time()))
    # 已经包含/api/movie元素的列表里面添加时间戳
    args.append(timestamp)
    # 列表中元素使用,进行拼接，然后进行 SHA1 编码
    sign = hashlib.sha1(','.join(args).encode('utf-8')).hexdigest()
    # 编码的结果和时间戳再次拼接，拼接后的结果再进行 Base64 编码
    return base64.b64encode(','.join([sign, timestamp]).encode('utf-8')).decode('utf-8')

# 先将 /api/movie 放到一个列表里面， /api/movie 是生成token值的一个参数
args = ['/api/movie']
token = get_token(args=args)
# 获取列表页地址
index_url = INDEX_URL.format(limit=LIMIT, offset=OFFSET, token=token)

# 列表页访问，获取一个列表页的内容，返回数据json格式
response = requests.get(index_url)
print('response', response.json())
print('*' * 100 )

# 返回的json格式字符串转变为python格式
result = response.json()
# 每部电影放在result里面的results里面，results是一个列表，里面的每部电影是一个字典，参考图片039
for item in result['results']:
    # 电影的id
    id = item['id']
    # 加密后的id，就是初始固定字符串拼接电影ID（转变为字符串后再拼接）然后base64编码
    encrypt_id = base64.b64encode((SECRET + str(id)).encode('utf-8')).decode('utf-8')
    # 电影详情页的token构造逻辑和列表页的token构造方法一样，不过多传入了加密后的id，列表页只传入了/api/movie
    args = [f'/api/movie/{encrypt_id}']
    token = get_token(args=args)
    # 获取详情页地址.
    detail_url = DETAIL_URL.format(id=encrypt_id, token=token)
    response = requests.get(detail_url)
    print('response', response.json())
