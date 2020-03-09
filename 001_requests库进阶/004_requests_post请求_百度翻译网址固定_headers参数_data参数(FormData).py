# -*- coding:utf-8 -*-

# 百度翻译,post请求
# 翻译接口网址固定：https://fanyi.baidu.com/v2transapi

import requests
import json

url = "https://fanyi.baidu.com/v2transapi"
# 传入的请求头信息都需要使用字典格式
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0"}
# 参数根据网址规则传入，字典格式
# 火狐浏览器抓包后分析post请求，表单数据有很多，我们一般只取前面关键的
# 后面的sign和token都是每次生成的数据，每次都不同，放在这里会请求失败
form_data = {
    "query": "人生苦短",
    "from": "zh",
    "to": "en",
}

# 使用post请求，传入网址，请求头，表单参数(FormData)
response = requests.post(url=url, headers=headers, data=form_data)

# 查看返回的请求内容
print(response.status_code)
print(response.content.decode())

# 响应内容是json数据，json下载为python中的字典格式
dict_ret = json.loads(response.content.decode())
# 取出翻译结果，字典中的字典中
# ret = dict_ret["trans"][0]["dst"]
# print(ret)

# 注意：百度翻译接口会随时修改，上述代码会失效
