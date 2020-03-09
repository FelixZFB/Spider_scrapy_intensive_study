# -*- coding:utf-8 -*-

import requests

# 模拟人人网登录，先登陆一次，
# 获取保存cookie，之后就可以自动携带cookie登录

# 使用session发送一次请求，获取cookie
def login():
    # 1 实例化一个session对象
    session = requests.session()

    # 2 第一次post请求，要传入登陆账号和密码
    post_url = "http://www.renren.com/PLogin.do"
    form_data = {'email': '908851835@qq.com', 'password': 'zfb123456zfb'}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3730.400 QQBrowser/10.5.3805.400"}
    # 使用上面的实例session发送post请求，传入上面的参数
    session.post(url=post_url, headers=headers, data=form_data)
    # 上面发送一次请求以后，session实例就已经有了cookie

    # 3 直接登录主页，login()要在该函数之前执行一次,直接使用get请求
    # 如果直接requests.get请求个人主页，由于没有cookie，会自动跳转到登陆页面
    home_page_url = "http://www.renren.com/574862780/profile"
    response = session.get(url=home_page_url, headers=headers)

    # 输出结果就有个人信息
    print(response.status_code)
    print(response.content.decode())

if __name__ == "__main__":
    login()

# 关于POST地址查找：
#