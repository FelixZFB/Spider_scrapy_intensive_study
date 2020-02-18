# -*- coding:utf-8 -*-

import requests

url = "https://www.baidu.com"
# 传入的请求头信息都需要使用字典格式
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0"}

# 使用get请求，传入网址，请求头
response = requests.get(url=url, headers=headers)

print(response.status_code)

# 解码类型：根据HTTP 头部对响应的编码作出有根据的推测，推测的文本编码
# 可以指定编码
# 类型：str
response.encoding = "utf-8"
print(type(response.text))


# - 类型：bytes
# - 解码类型： 没有指定,默认utf-8
# - 如何修改编码方式：response.content.decode(“utf-8”)
print(type(response.content))
print(type(response.content.decode()))


# 使用response.text 时，Requests 会基于 HTTP 响应的文本编码自动解码响应内容，大多数 Unicode 字符集都能被无缝地解码。
# 使用response.content 时，返回的是服务器响应数据的原始二进制字节流，可以用来保存图片等二进制文件。

# requests默认自带的Accept-Encoding导致或者网站默认发送的就是压缩之后的网页
# 但是为什么content.read()没有问题，因为requests，自带解压压缩网页的功能
# 当收到一个响应时，Requests会猜测响应的编码方式，用于在你调用response.text方法时对响应进行解码。
# Requests首先在HTTP头部检测是否存在指定的编码方式，如果不存在，则会使用chardet.detect来尝试猜测编码方式（存在误差）
# 更推荐使用response.content.decode()
