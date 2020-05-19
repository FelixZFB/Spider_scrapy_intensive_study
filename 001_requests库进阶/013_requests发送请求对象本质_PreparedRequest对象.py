# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/19 21:59
Desc:
'''

from requests import Request, Session

url = 'http://httpbin.org/post'
data = {'name': 'germany'}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
}

# 然后用 url、data 和 headers 参数构造了一个 Request 对象，
# 这时需要再调用 Session 的 prepare_request 方法将其转换为一个 Prepared Request 对象，
# 然后调用 send 方法发送,返回response对象

s = Session()
req = Request('POST', url, data=data, headers=headers)
prepped = s.prepare_request(req)
r = s.send(prepped)

print(type(req))
print(type(prepped))
print(type(r))
print(r.text)