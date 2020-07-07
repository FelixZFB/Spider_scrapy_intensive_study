# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/7/7 16:56
Desc:
'''

import requests
from urllib.parse import urljoin

# 登陆前的主页地址
BASE_URL = 'https://login3.scrape.cuiqingcai.com/'
# 登陆请求的post地址
LOGIN_URL = urljoin(BASE_URL, '/api/login')
# 登录后的地址
INDEX_URL = urljoin(BASE_URL, '/api/book')
# 用户名和密码
USERNAME = 'admin'
PASSWORD = 'admin'

# 发送登陆请求
response_login = requests.post(LOGIN_URL, json={
   'username': USERNAME,
   'password': PASSWORD
})

# 返回登陆成功后返回的json数据，json()方法得到的是一个python字典
data = response_login.json()
print(type(data))
print('Response JSON：', data)
# 获取返回的json数据的json的值,即jwt的值
jwt = data.get('token')
print('JWT: ', jwt)

# 再次请求的时候，jwt值是放在Authorization字段的值中，字段前面需要添加jwt
headers = {
   'Authorization': f'jwt {jwt}'
}

# 携带jwt访问，limit和offset是访问网址？后面的参数，限制每页显示的图书数量
response_index = requests.get(INDEX_URL, params={
   'limit': 18,
   'offset': 0
}, headers=headers)
print('Response Status', response_index.status_code)
print('Response URL', response_index.url)
print('Response Data', response_index.json())