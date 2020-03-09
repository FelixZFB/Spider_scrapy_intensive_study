# -*- coding:utf-8 -*-

import requests
import retrying

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3730.400 QQBrowser/10.5.3805.400",
}

# 有时候加入超时，但是网络出现问题，请求一次可能失败了
# 加入重试模块功能,该函数循环执行3次，然后继续执行之后代码
# 该模块实际就是执行了下面try函数的异常捕获功能，只有错误时候才会执行三次，如果请求成功就只有一次
@retrying.retry(stop_max_attempt_number=3)
def _parse_url(url):
    print("*" * 100) # 看执行了几次
    response = requests.get(url, headers=headers, timeout=3)
    assert response.status_code == 200
    return response.content.decode()

def parse_url(url):
    try:
        html_str = _parse_url(url)
    except:
        html_str = None
    return html_str

if __name__ == "__main__":
    url = "https://www.123baidu.com/"
    ret = parse_url(url)
    print(ret)
