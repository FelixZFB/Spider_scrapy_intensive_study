# -*- coding:utf-8 -*-

# url带参数的请求格式为（举例）： http://www.baidu.com/s?k1=v1&k2=v2
# 当请求数据为字典data = {k1:v1, k2:v2}，且参数中包含中文或者？、=等特殊符号时，
# 通过url编码，将data转化为特定格式k1=v1&k2=v2，并且将中文和特殊符号进行编码，避免发生歧义

# 直观看见的网址，复制粘贴到浏览器中打开会找不到URL地址
# https://www.baidu.com/baidu?wd=熊猫
# URL编码后的地址
# https://www.baidu.com/baidu?wd=%E7%86%8A%E7%8C%AB

import requests
from urllib import parse
from urllib import request

url = 'http://www.baidu.com/s?'
dict1 ={'wd': '熊猫'}
# 将字典参数进行URL编码
url_data = parse.urlencode(dict1) #unlencode()将字典{k1:v1,k2:v2}转化为k1=v1&k2=v2
print(url_data)             #url_data：wd=%E7%99%BE%E5%BA%A6%E7%BF%BB%E8%AF%91

# 编码后的地址直接进行拼接，然后打开
data = request.urlopen((url+url_data)).read() #读取url响应结果
# 直接获取的数据是字节格式，字节采用utf-8进行解码
data = data.decode('utf-8')

# URL地址进行解码
url_org = parse.unquote(url_data) #解码url
print(url_org)
print(requests.utils.unquote(url_data))
print("*" * 100)


# URL编码也可以使用以下方式
str1 = 'haha哈哈'
str2 = parse.quote(str1)    #将字符串进行编码
print(str2)                 #str2=haha%E5%93%88%E5%93%88
str3 = parse.unquote(str2)  #解码字符串
print(str3)                 #str3=haha哈哈


