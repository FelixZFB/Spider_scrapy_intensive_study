# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
from urllib import parse

# 用于py里面直接启动爬虫
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# RedisSpider分布式爬虫相对于普通scrapy_redis爬虫(jbbook爬虫是普通的scrapy_redis增量式爬虫)需要修改以下3个内容
from scrapy_redis.spiders import RedisSpider # 1 导入RedisSpider爬虫模块


class DangdangSpider(RedisSpider): # 2 修改爬虫继承的类
    name = 'dangdang'
    allowed_domains = ['dangdang.com']
    # start_urls = ['http://book.dangdang.com/']
    redis_key = 'dangdang:start_url' # 3 设置redis_key键的名称，用于启动爬虫后，传入值(值就是要爬取的start_urls）

    def parse(self, response):
        # 大分类(一级分类)
        div_list = response.xpath('.//div[@class="con flq_body"]/div')
        for div in div_list: # 取出大分类列表下的每一个大分类
            item = dict() # 每次循环大分类时候创建一个新的item，后面分类里面的item需要使用deepcopy，不然新建时候会覆盖掉以前的数据
            item['b_cate'] = div.xpath('./dl/dt//text()').extract() # 注意：大分类文字查看元素是放在dt下面span标签下多个a标签里面，但是response实际是没有span标签的，此处直接使用//text()取出dt标签下的所有文字内容，结果是一个列表
            item['b_cate'] = [i.strip() for i in item['b_cate'] if len(i.strip()) > 0] # 取出文字内容两端的换行及空白内容，保留实际长度大于0的内容，去掉列表中的空元素
            # 中间分类(二级分类)分组,网页元素以文艺为例进行查看
            dl_list = div.xpath('./div//dl[@class="inner_dl"]')
            for dl in dl_list:
                item['m_cate'] = dl.xpath('./dt//text()').extract() # 文字有些直接在dt标签下面，有些是在dt下面的a标签下面
                item['m_cate'] = [i.strip() for i in item['m_cate'] if len(i.strip()) > 0] # 去除两端空格
                # 小分类(三级分类)分组
                s_list = dl.xpath('./dd/a')
                for s in s_list:
                    item['s_cate'] = s.xpath('./text()').extract_first().strip() # 注意查看元素a下面有span标签，实际源码是没有span标签，文字内容直接在a标签下面
                    item['s_href'] = s.xpath('./@href').extract_first()
                    # 从小分类进去图书列表，获取图书的具体信息
                    if item['s_href'] is not None:
                        yield scrapy.Request(
                            url=item['s_href'],
                            meta={'item': deepcopy(item)}, # 注意此处传递的item是每次开始一个新的item循环后传递的，需要deepcopy
                            callback=self.parse_book_list
                        )


    def parse_book_list(self, response):
        item = response.meta['item']
        # 图书列表获取
        li_list = response.xpath('.//ul[@class="bigimg"]/li')
        for li in li_list: # 取出每一本图书，获取图书的具体信息
            item['book_href'] = li.xpath('./a/@href').extract_first()
            item['book_img'] = li.xpath('./a[@class="pic"]/img/@data-original').extract_first() # 图片的src属性在response中并不是真实地址，<img data-original='http://img3m0.ddimg.cn/28/30/24198400-1_b_4.jpg' src='images/model/guan/url_none.png'
            item['book_name'] = li.xpath('./p[@class="name"]/a/@title').extract_first()
            item['book_desc'] = li.xpath('./p[@class="detail"]/text()').extract_first()
            item['book_price'] = li.xpath('.//span[@class="search_now_price"]/text()').extract_first() # 价格有多个，只要当前售价
            item['book_author'] = li.xpath('./p[@class="search_book_author"]/span[1]/a/text()').extract()  # 作者有多个放在span下多个a标签里面,全部取出结果是一个列表
            item['book_publish_date'] = li.xpath('./p[@class="search_book_author"]/span[2]/text()').extract_first()
            item['book_press'] = li.xpath('./p[@class="search_book_author"]/span[3]/a/text()').extract_first()
        # 在爬取最后一级使用yield返回item内容，爬取窗口里面也会显示爬取结果
        # 不yield或者print爬虫里面只会显示爬取过程，并不会显示items内容
        yield item

        # 爬取下一页，进行翻页
        next_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_url is not None:
            next_url = parse.urljoin(response.url, next_url)
            yield scrapy.Request(
                url=next_url,
                meta={'item': item}, # 此处还没有开始新的item循环，不用deepcopy
                callback=self.parse_book_list
            )


# 命令行scrapy crawl dangdang可以启动爬虫，
# 我们也可以添加爬虫启动程序process，使用以下三行代码启动爬虫
# 启动爬虫，爬虫处于监听状态，然后redis客户端传入起始url命令：lpush dangdang:start_url http://book.dangdang.com/
if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('dangdang')
    process.start()


