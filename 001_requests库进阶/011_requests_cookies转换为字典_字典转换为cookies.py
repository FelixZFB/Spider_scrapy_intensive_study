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
    response = session.post(url=post_url, headers=headers, data=form_data)

    print(response.cookies)
    print("*" * 100)

    # 将cookies转换为字典
    dict = requests.utils.dict_from_cookiejar(response.cookies)
    print(dict)
    print("*" * 100)

    # 将字典转换为cookies
    print(requests.utils.cookiejar_from_dict(dict))
    print("*" * 100)


if __name__ == "__main__":
    login()

# 关于POST地址查找：
#