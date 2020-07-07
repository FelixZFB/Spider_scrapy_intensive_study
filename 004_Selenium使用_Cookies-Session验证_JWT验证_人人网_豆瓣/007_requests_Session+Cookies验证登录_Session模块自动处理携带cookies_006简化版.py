# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/7/7 15:12
Desc:
'''
# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/7/7 11:32
Desc:
'''

# requests 默认情况下每次请求都是独立互不干扰的，比如我们第一次先调用了 post 方法模拟登录，
# 然后紧接着再调用 get 方法请求下主页面，其实这是两个完全独立的请求，
# 第一次请求获取的 Cookies 并不能传给第二次请求

# 因此，需要先模拟登录请求，获取的登录后本地浏览器保存到的cookies值
# 第二次登陆，headers里面携带上cookies值

import requests
from urllib.parse import urljoin

# 登陆前的主页地址
BASE_URL = 'https://login2.scrape.cuiqingcai.com/'
# 登陆请求的post地址
LOGIN_URL = urljoin(BASE_URL, '/login')
# 登录后的地址
INDEX_URL = urljoin(BASE_URL, '/page/1')
# 用户名和密码
USERNAME = 'admin'
PASSWORD = 'admin'

# requests 内置的 Session 对象来帮我们自动处理 Cookies，
# 使用了 Session 对象之后，requests 会将每次请求后需要设置的 Cookies 自动保存好，
# 并在下次请求时自动携带上去，就相当于帮我们维持了一个 Session 对象
session = requests.Session()

# 登陆请求，请求需要使用session对象
response_login = session.post(LOGIN_URL, data={
   'username': USERNAME,
   'password': PASSWORD
}, allow_redirects=False)

# 使用session对象管理已经获取到cookies，下次请求该域名下的地址自动携带cookies
cookies = session.cookies
print('Cookies：', cookies)

# 第二次请求，携带本地已有的cookies值
# requests库自带了CookieJar功能，get请求直接使用CookieJar获取的cookies传入
# 本地已有了cookies，需要使用headers的Cookie参数传入，参考000_43_12案例
# 000_43案例中使用的request库，需要手动设置cookies放在headers里面，或者使用cookiejar模块

# 请求需要使用session对象
response_index = session.get(INDEX_URL)
print('Response Status：', response_index.status_code)
print('Response URL：', response_index.url)