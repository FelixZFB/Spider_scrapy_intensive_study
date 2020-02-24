# -*- coding: utf-8 -*-
import scrapy
from tieba.items import TiebaItem
from urllib.parse import urljoin



# 用于py里面直接启动爬虫
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class TbSpider(scrapy.Spider):
    name = 'tb'
    allowed_domains = ['tieba.com']
    start_urls = ['https://tieba.baidu.com/f?kw=akg&ie=utf-8']

    def parse(self, response):
        # 先取出所有帖子所在的li标签列表
        li_list = response.xpath('.//ul[@id="thread_list"]/li')
        for li in li_list[1:]:
            title = li.xpath('./div/div[2]/div[1]/div[1]/a/text()').extract_first()
            href = li.xpath('./div/div[2]/div[1]/div[1]/a/@href').extract_first()
            if href is not None:
                # 网址补充完整的两种常用方式，第二种方式是scrapy自带的，方法里面已经有默认的response.url参数了
                # href = urljoin(response.url, href)
                href = response.urljoin(href)
            print(title,href)




# 命令行scrapy crawl tb可以启动爬虫，
# 我们也可以添加爬虫启动程序process，使用以下三行代码启动爬虫
if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('tb')
    process.start()


