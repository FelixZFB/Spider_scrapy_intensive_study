# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random


# 默认自动创建的爬虫中间件
class CricSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

# 默认自动创建的下载中间件
class CricDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# 自定义中间件，定义完成后需要return返回request或者response交给下载器或者爬虫去处理
# 自定义完成后，需要在settings的中间件位置进行设置启动
class RandomUserAgentMiddleware():
    # process_request是一个默认方法，当每一个request通过该中间件时候都会启动该方法
    # request由引擎传递给下载器时候，经过该中间件，执行该方法，处理后的request(已经在请求头里面带上了代理)交给下载器进行下一步处理
    def process_request(self, request, spider):
        # spider.settings.get方法就可以从settings中取出USER_AGENTS_LIST列表
        ua = random.choice(spider.settings.get("USER_AGENTS_LIST"))
        # 使用ua代理请求网页
        request.headers["User-Agent"] = ua

class CheckUserAgentMiddleware():
    # process_response是一个默认方法，当每一个response通过该中间件时候都会启动该方法
    # 使用上面的代理请求，网页，此处返回请求后的response，处理后的响应传递给引擎进行下一步处理
    def process_response(self, request, response, spider):
        # 此处可以打印出来用于请求的UA，每次都是变化的
        # print(request.headers["User-Agent"])
        return response