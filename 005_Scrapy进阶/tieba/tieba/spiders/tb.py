# -*- coding: utf-8 -*-
import scrapy
from tieba.items import TiebaItem
from urllib.parse import urljoin

# 用于py里面直接启动爬虫
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class TbSpider(scrapy.Spider):
    name = 'tb'
    # 主域名不是tieba.com，写错了，只会爬取start_urls即贴吧第一页，第二页开始就被过滤了，就不会向下爬取了，
    # 当时就写错掉坑了，检查半天才发现，allowed_domains详细解释查看005_Scrapy进阶学习.MD中的笔记
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['https://tieba.baidu.com/f?kw=akg&ie=utf-8']

    def parse(self, response):
        # 先取出所有帖子所在的li标签列表
        tieba_name = response.xpath('.//a[@class=" card_title_fname"]/text()').extract_first().strip()
        li_list = response.xpath('.//ul[@id="thread_list"]/li')
        # 第一页有置顶的帖子，由于不满足下面规则，会自动过滤掉
        for li in li_list:
            title = li.xpath('./div/div[2]/div[1]/div[1]/a/text()').extract_first()
            author = li.xpath('./div/div[2]/div[1]/div[2]/span[1]/span[1]/a/text()').extract_first()
            href = li.xpath('./div/div[2]/div[1]/div[1]/a/@href').extract_first()
            if href is not None:
                # 网址补充完整的两种常用方式，第二种方式是scrapy自带的，方法里面已经有默认的response.url参数了
                # 直接import urllib  然后使用：urllib.parse.urljoin() 识别不了parse，原因未知
                href = urljoin(response.url, href)
                # href = response.urljoin(href)

                item = TiebaItem(tieba_name=tieba_name, title=title, author=author, href=href)
                print(item)

                yield scrapy.Request(
                    url=href,
                    callback=self.parse_detail,
                    meta={"item": item}
                )


        # 爬取下一页,调用的还是parse方法
        next_url = response.xpath('.//a[@class="next pagination-item "]/@href').extract_first()
        print(next_url)
        if next_url is not None:
            next_url = urljoin(response.url, next_url)
            print(next_url)
            yield scrapy.Request(url=next_url, callback=self.parse)
        else:
            print("数据提取完成!")


    def parse_detail(self, response):
        item = response.meta['item']
        # 取出帖子回复数，回复数帖子开头和末尾都出现了，样式是唯一的，取出第一个即可，可以使用extract_first()，下面使用列表取出
        item['reply_num'] = response.xpath('.//span[@style="margin-right:3px"]/text()').extract()[0]
        yield item


# 命令行scrapy crawl tb可以启动爬虫，
# 我们也可以添加爬虫启动程序process，使用以下三行代码启动爬虫
if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('tb')
    process.start()


