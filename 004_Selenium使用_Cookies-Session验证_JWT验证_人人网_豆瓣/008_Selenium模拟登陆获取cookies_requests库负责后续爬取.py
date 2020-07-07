# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/7/7 15:38
Desc:
'''

from urllib.parse import urljoin
from selenium import webdriver
import requests
import time

# 登陆前的主页地址
BASE_URL = 'https://login2.scrape.cuiqingcai.com/'
# 登陆请求的post地址
LOGIN_URL = urljoin(BASE_URL, '/login')
# 登录后的地址
INDEX_URL = urljoin(BASE_URL, '/page/1')
# 用户名和密码
USERNAME = 'admin'
PASSWORD = 'admin'

# Selenium模拟登陆，等待一定时间，确保登陆成功
browser = webdriver.Chrome()
browser.get(BASE_URL)
browser.find_element_by_css_selector('input[name="username"]').send_keys(USERNAME)
browser.find_element_by_css_selector('input[name="password"]').send_keys(PASSWORD)
browser.find_element_by_css_selector('input[type="submit"]').click()
time.sleep(3)

# 使用selenium取出cookies
# get cookies from selenium
cookies = browser.get_cookies()
# selenium取出的cookies是字典形式，里面有很多参数，我们只需要name和value的值
print('Cookies: ', cookies)
browser.close()

# 使用selenium取出的cookies值，只需要字典里面的name和value的值
# Cookies:  [{'domain': 'login2.scrape.cuiqingcai.com', 'expiry': 1595317458.177094, 'httpOnly': True, 'name': 'sessionid', 'path': '/', 'secure': False, 'value': 'o3cctl1fbeedt3q3m3bg6nlxtv0m9os7'}]
# set cookies to requests
session = requests.Session()
for cookie in cookies:
   session.cookies.set(cookie['name'], cookie['value'])

print(session.cookies)

response_index = session.get(INDEX_URL)
print('Response Status', response_index.status_code)
print('Response URL', response_index.url)

# 运行结果：
# Cookies:  [{'domain': 'login2.scrape.cuiqingcai.com', 'expiry': 1595317458.177094, 'httpOnly': True, 'name': 'sessionid', 'path': '/', 'secure': False, 'value': 'o3cctl1fbeedt3q3m3bg6nlxtv0m9os7'}]
# <RequestsCookieJar[<Cookie sessionid=o3cctl1fbeedt3q3m3bg6nlxtv0m9os7 for />]>
# Response Status 200
# Response URL https://login2.scrape.cuiqingcai.com/page/1