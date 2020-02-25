# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

# 用于py里面直接启动爬虫
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class TtSpider(CrawlSpider):
    name = 'tt'
    allowed_domains = ['tencent.com']
    start_urls = ['https://careers.tencent.com/search.html']

    rules = (
        # 寻找下一页的规律，开始爬取后，会在第一页寻找下一页的地址，然后第二页继续寻找下一页地址，实际寻找的就是列表页
        Rule(LinkExtractor(allow=r'/search.html\?index=\d'), callback='parse_item', follow=True),
    )

    # 列表页数据提取
    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        item['title'] = response.xpath('//div[@class="work-title"]/text()').extract_first()
        print(item)
        return item

    # 详情页数据提取
    def parse_detail(self, response):
        pass


# 命令行scrapy crawl tt可以启动爬虫，
# 我们也可以添加爬虫启动程序process，使用以下三行代码启动爬虫
if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('tt')
    process.start()