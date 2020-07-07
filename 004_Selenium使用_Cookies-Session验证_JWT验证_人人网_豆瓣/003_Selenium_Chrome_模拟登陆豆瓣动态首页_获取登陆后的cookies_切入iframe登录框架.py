# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
Date: 2019/9/25 16:59
Desc:
'''

import time
from selenium import webdriver

def douban_login():

    # 创建一个浏览器驱动实例
    driver = webdriver.Chrome()
    # 请求网页
    url = "https://www.douban.com/"
    driver.get(url)
    # print("Title: {0}".format(driver.title))
    # 切换到iframe框架中，可以先找到所有的iframe标签列表，然后使用标签的位置
    # 如果iframe有name属性，可以直接传入name属性值
    # 比如QQ邮箱的登陆模块driver.switch_to.frame("login_frame")
    driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])

    # driver.switch_to.default_content()或driver.switch_to.parent_frame()，切换到外层默认框架

    driver.find_element_by_xpath("/html/body/div[1]/div[1]/ul[1]/li[2]").click()
    time.sleep(5)

    # 发送用户名和密码，需要更改为自己的用户名和密码
    driver.find_element_by_id("username").send_keys("用户名")
    driver.find_element_by_id("password").send_keys("密码")
    time.sleep(3)

    # 点击登录豆瓣
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[5]/a").click()

    # 获取登录后的原始cookies信息
    print("driver.get_cookies()获取到的原始cookies:%s" % driver.get_cookies())

    # 下面取出的是浏览器response中cookies的值,格式化后的值，看003图片
    cookies = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}
    print("*" * 100)
    print(cookies)

    
    # 关闭浏览器
    driver.close()

if __name__ == '__main__':
    douban_login()