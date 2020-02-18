# -*- coding:utf-8 -*-

import requests

# 方式1：直接将cookie放在请求头中

cookies = "anonymid=k06r6sdauyh36v; depovince=ZGQT; _r01_=1; JSESSIONID=abcOraT1E7z0JhHDATb0w; ick_login=8f53ebf1-b972-4572-8f77-810953dcfdfe; first_login_flag=1; ln_uact=908851835@qq.com; ln_hurl=http://hdn.xnimg.cn/photos/hdn221/20131218/1650/original_RrRf_470e00037cf7111a.jpg; jebecookies=0f21ab0f-a7a8-4467-9bbc-13110c7a411f|||||; _de=24AF6279ED439B973399691954C56086696BF75400CE19CC; p=3ae05d78f7e97e1518aaee67caf5b2280; ap=574862780; t=495e85781ac79a4cc7e2ec9553006bb50; societyguester=495e85781ac79a4cc7e2ec9553006bb50; id=574862780; xnsid=fe384fe8; ver=7.0; loginfrom=null; wp_fold=0"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3730.400 QQBrowser/10.5.3805.400",
    "Cookie": cookies,
}


home_page_url = "http://www.renren.com/574862780/profile"
response = requests.get(url=home_page_url, headers=headers)
print(response.text)

# 输出结果有<title>人人网 - 夏树柏</title>
