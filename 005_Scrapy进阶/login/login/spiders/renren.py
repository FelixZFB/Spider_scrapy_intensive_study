# -*- coding: utf-8 -*-
import scrapy
import re

# 用于py里面直接启动爬虫
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class RenrenSpider(scrapy.Spider):
    # 人人网：908851835@qq.com  zfb123456zfb
    name = 'renren'
    allowed_domains = ['renren.com']
    start_urls = ['http://renren.com/']

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response, # 自动从start_urls中寻找登陆form表单进行登陆
            # 实际真正的登录url是：http://www.renren.com/PLogin.do
            # scrapy会通过start_urls去寻找真正的登录地址
            # 运行结果可以看见先请求'http://renren.com/'，然后里面找到http://www.renren.com/PLogin.do
            formdata={
                "email": "908851835@qq.com",
                "password": "zfb123456zfb"
            },
            callback=self.parse_page # 登录成功之后的处理
        )

    def parse_page(self, response):
        # 我的个人主页就是：http://www.renren.com/574862780
        print(response.url, "\n", response.status)
        print("*" * 100)
        # 查看响应里面是否有我的用户名
        print(re.findall(r"夏树柏", response.text))


# 命令行scrapy crawl renren可以启动爬虫，
# 我们也可以添加爬虫启动程序process，使用以下三行代码启动爬虫
if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('renren')
    process.start()

# 运行部分结果：
# [scrapy.downloadermiddlewares.redirect] DEBUG: Redirecting (302) to <GET http://www.renren.com/home> from <POST http://www.renren.com/PLogin.do>

# http://www.renren.com/574862780
# 200
# ['夏树柏', '夏树柏', '夏树柏', '夏树柏', '夏树柏']