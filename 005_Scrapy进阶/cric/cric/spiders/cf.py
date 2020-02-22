# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from cric.items import CricItem
import re
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class CfSpider(CrawlSpider):
    name = 'cf'
    allowed_domains = ['bxjg.circ.gov.cn']
    # 保监会处罚作为首页，该url地址里面的response就有每个处罚的url地址
    start_urls = ['http://bxjg.circ.gov.cn/web/site0/tab5240/module14430/page1.htm']

    # 定义提取url地址规则，Rule一个规则集合
    rules = (
        # LinkExtractor 连接提取器，提取url地址，提取方法是正则
        # callback 提取出来url地址的response会交给callback的方法处理
        # follow 当前的url地址的response继续进rules里面的规则继续提取url地址
        # 每个详情页的网址就是info后面的数字不同，直接传入\d+，匹配多个数字，\.就代表.,详情页不需要向下继续提取url，follow不需要
        Rule(LinkExtractor(allow=r'/web/site0/tab5240/info\d+\.htm'), callback='parse_item'),
        # 寻找下一页的规则，请求start_urls后，自动根据规则寻找下一页的地址并去请求,不断从新的一页继续寻找下一页，但是不需要callback
        # 每一页里面的response里面的内容列表满足上面rule规则，就会自动请求进去提取内容
        Rule(LinkExtractor(allow=r'/web/site0/tab5240/module14430/page\d+\.htm'), follow=True),
    )

    #
    def parse_item(self, response):
        #item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        #return item
        title = re.findall("<!--TitleStart-->(.*?)<!--TitleEnd-->", response.text)[0]
        publish_date = re.findall("发布时间：20\d{2}-\d{2}-\d{2}", response.text)[0]

        item = CricItem(title=title, publish_date=publish_date)
        yield item


# 命令行可以启动爬虫，我们也可以添加爬虫启动程序process，使用以下三行代码启动爬虫
if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('cf')
    process.start()
