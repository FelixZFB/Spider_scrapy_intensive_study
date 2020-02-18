# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
Date: 2019/9/16 20:23
Desc:
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main():
    # 设置无界面浏览器,取消该设置，浏览器会自动打开操作
    options = Options()
    options.add_argument('-headless')

    # 创建一个实例无界面浏览器实例
    driver = webdriver.Chrome(options=options)
    driver.get('http://www.baidu.com')
    print("Title: {0}".format(driver.title))

    # 关闭浏览器
    driver.close()

if __name__ == '__main__':
    main()