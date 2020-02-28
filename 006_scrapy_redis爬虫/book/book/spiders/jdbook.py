# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import json

# 用于py里面直接启动爬虫
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# 打造分布式爬虫
from scrapy_redis.spiders import RedisSpider

class JdbookSpider(scrapy.Spider):
    name = 'jdbook'
    allowed_domains = ['jd.com', 'p.3.cn']
    start_urls = ['https://book.jd.com/booksort.html'] # 通过分析找到所有图书分类作为起始URL

    def parse(self, response):
        dt_list = response.xpath('//div[@class="mc"]/dl/dt') # 图书大分类列表,所有大分类都放在dt标签
        # 注意item：我们是在每次循环一个大分类时候才新建一个空的item字典,循环一次都是共用的一个大的item
        # 每开始一个新的循环就新建了item字典，之前的item就会没有了，所以下面的item需要使用deepcopy深拷贝
        # 深拷贝后item就是一个新的地址了，不会影响之前已经生成的item内容，最终爬虫结束实际生成了很多个item
        # item在parse里面创建后，先传到parse_book_list，然后传到parse_book_price相当于是最后一级
        # 到最后一级了，返回item，由于前面都是deepcopy地址都是新的了，下个循环对已有的item就不会产生影响了
        # 如果不使用item = dict()的方式，可以现在items.py里面定义各个字段，这边每次传过去即可，参考以前的案例
        # 图书大分类里面取出图书每一个大分类
        for dt in dt_list:
            item = dict()
            item['b_cate'] = dt.xpath('./a/text()').extract() # 大分类名称，注意，是从dt下面开始取不是response，当时写成response肯定就找不到了
            # ./表示选定当前标签，following-sibling::dd[1]表示向后取兄弟标签，取第一个dd标签
            # 大分类下的小分类列表，一个大分类紧邻的兄弟标签就是小分类列表
            em_list = dt.xpath('./following-sibling::dd[1]/em')
            # 小分类列表循环取出每个小分类，然后请求小分类，进入后就是具体的图书列表
            for em in em_list:
                item['s_href'] = em.xpath('./a/@href').extract_first() # 小分类的连接
                item['s_cate'] = em.xpath('./a/text()').extract_first() # 小分类名称
                # 小分类存在的时候，构造请求
                if item['s_href'] is not None:
                    item['s_href'] = response.urljoin(item['s_href']) # 实用scrapy自带的urljoin拼接网址
                    yield scrapy.Request(
                        url=item['s_href'],
                        callback=self.parse_book_list,
                        meta={'item': deepcopy(item)}
                    )


    # 解析每个小分类下的图书列表页
    def parse_book_list(self, response):
        item = response.meta['item']
        # 进入小分类后，先获取一页的图书列表
        li_list = response.xpath('//div[@id="plist"]/ul/li')
        for li in li_list:
            # 图片的连接需要拼接完整,图片地址有些书籍有问题有些没有
            item['book_img'] = "https:" + li.xpath('.//div[@class="p-img"]/a/img/@src').extract_first() # 获取图书封面连接，.//当前标签下的任意位置，都用属性在li标签下面查找
            item['book_name'] = li.xpath('.//div[@class="p-name"]//em/text()').extract_first().strip() # name的文字放在em标签下面多个font标签，em/text()表示取出em标签下所有的文字内容，两端的空格去除
            item['book_href'] = response.urljoin(li.xpath('.//div[@class="p-name"]/a/@href').extract_first()) # 去除文字两端的空格
            item['book_author'] = li.xpath('.//span[@class="author_type_1"]/a/text()').extract() # 注意有些作者有多个，所以取出a标签的所有文字内容
            item['book_publish'] = li.xpath('.//span[@class="p-bi-store"]/a/text()').extract_first() # 出版社
            book_publish_date = li.xpath('.//span[@class="p-bi-date"]/text()').extract_first() # 出版日期
            if book_publish_date is not None: # 注意有些出版日期是None值，不支持使用strip()方法先要判断一下
                item['book_publish_date'] = book_publish_date.strip()
            # 图书的价格是JS动态获取到的，JS请求时候需要使用图书的skuID实际就是图书的ID号码
            # 需要先获取真实的请求地址，分析过程查看005_Scrapy进阶学习中## 3.5 京东图书爬虫分析过程
            item['book_skuID'] = li.xpath('./div/@data-sku').extract_first()
            yield scrapy.Request(
                url='https://p.3.cn/prices/mgets?skuIds=J_{}'.format(item['book_skuID']), # 注意价格域名和上面允许的域名不同，需要把价格域名加到上面去
                callback=self.parse_book_price,
                meta={'item': deepcopy(item)}
            )

        # 图书列表页获取下一页
        next_url = response.xpath('//a[@class="pn-next"]/@href').extract_first()
        if next_url is not None:
            yield scrapy.Request(
                url=response.urljoin(next_url), # 网址需要拼接完整
                callback= self.parse_book_list, # 下一页继续解析图书清单
                # 此处的item还是在上面新建一个item = dict()的内部，一个item还没有循环结束，需要内部继续传递
                meta = {'item': item}  # 此处需要传递item，不然会报48行的KEYERROR错误
            )

    # 获取图书的价格信息
    def parse_book_price(self, response):
        item = response.meta['item']
        item['book_price'] = json.loads(response.text)[0]['op']
        print(item)



# 命令行scrapy crawl jdbook可以启动爬虫，
# 我们也可以添加爬虫启动程序process，使用以下三行代码启动爬虫
if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('jdbook')
    process.start()
