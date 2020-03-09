# -*- coding:utf-8 -*-
# 002案例可以直接使用字符串拼接更加简单

import requests
from urllib import parse

# 字符串拼接，requests.get会自动进行url编码
url = "https://www.baidu.com/baidu?wd={}".format("熊猫")

# 传入的请求头信息都需要使用字典格式
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0"}

# 使用get请求，传入网址，请求头
response = requests.get(url=url, headers=headers)

# 查看响应网址
print(response.url)
# url地址编码解码
print(parse.unquote(response.url))