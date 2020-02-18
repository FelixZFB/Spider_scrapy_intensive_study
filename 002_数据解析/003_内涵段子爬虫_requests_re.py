# -*- coding:utf-8 -*-

import requests
import re


class Neihan():
    def __init__(self):
        self.start_url = "http://www.neihanshu.net/text/index.html"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}

    def parse_url(self, url):
        response = requests.get(url=url, headers=self.headers)
        return response.content.decode()

    def get_page_content(self, html_str):
        # 内涵文字都是放在p标签中，但是只有只有前10个，re.S表示前面的字符串是普通字符串，里面的转义符都当做普通字符串
        content_list = re.findall(r"<p>(.*?)</p>", html_str, re.S)[0:10]
        return content_list

    def save_content_list(self, i, content_list):
        with open("003_内涵段子.txt", "a", encoding='utf-8') as f:
            for content in content_list:
                f.write(content.strip() + "\n" + "\n")
            print("第%s页保存成功" % i)

    def get_next_page_url(self, i):
        next_page_url = "http://www.neihanshu.net/text/index_{}.html".format(str(i))
        return next_page_url

    def run(self):
        # 1.start_url
        # 2.发送请求，获取响应内容
        html_str = self.parse_url(self.start_url)
        # 3.提取数据
        content_list = self.get_page_content(html_str)
        # 4. 保存数据
        self.save_content_list(1, content_list)
        # 5. 爬取保存下一页数据
        i = 1
        while True:
            i += 1
            # 重复上面的1234步骤
            next_page_url = self.get_next_page_url(i)
            html_str = self.parse_url(next_page_url)
            content_list = self.get_page_content(html_str)
            self.save_content_list(i, content_list)
            if i == 10:
                break


if __name__ == "__main__":
    neihan = Neihan()
    neihan.run()
