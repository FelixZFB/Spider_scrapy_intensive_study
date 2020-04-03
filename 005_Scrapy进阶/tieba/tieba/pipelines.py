# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import scrapy
from scrapy.exceptions import DropItem
import pymongo
from tieba.items import TiebaItem

class TiebaPipeline(object):
    # def process_item(self, item, spider):
    #     return item

    # 重写管道，用于下载存储数据到本地json文件
    def __init__(self):
        self.file = open('papers.json', 'w', encoding='utf-8')

    # 将ITEM里面的信息写入到一个json文件中
    def process_item(self, item, spider):
        # 判断item字典对象中title对应的是否还有值
        if item['title']:
            # 将item字典类型的数据转换成json格式的字符串, 每一个爬取一次(一个帖子)的结果的item，以一行写入，加上换行符
            # 注意json.dumps序列化时对中文默认使用的ascii编码，要想写入中文，加上ensure_ascii=False
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file.write(line)
            return item
        else:
            raise DropItem("Missing title in %s" % item)


# 自定义一个管道，用于将item数据存储到MongoDB数据库中
class MyTiebaPipeline(object):

    def __init__(self, mongo_uri, mongo_db, replicaset):

        # 设置mongDB的相关参数，只连接本地mongodb数据库，副本集相关代码注释掉
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.replicaset = replicaset

    @classmethod
    # 定义连接MongDB数据库的方法
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'tieba'),
            replicaset=crawler.settings.get('REPLICASET')
        )

    # 爬虫开启时候执行该函数，仅执行一次，连接数据库
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    # 爬虫关闭时候执行该函数，仅执行一次，关闭数据库连接
    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # 判断传过来的item(就是爬虫里面的jobListItem，最后yield jobListItem)是否属于JobListItem对象
        # 因为我们spiders文件夹可能有多个爬虫，items.py中也会自定义多个item的类，因此此处先进行一下判断
        if isinstance(item, TiebaItem):
            # 对item进行处理，调用处理的方法
            self._process_joblist_item(item)
        else:
            pass
        return item

    # 定义一个方法用于处理工作信息，插入数据到数据库
    def _process_joblist_item(self, item):
        '''
        处理小说信息
        :param item:
        :return:
        '''
        # 向数据库tieba中的tieba_akg表中插入item数据
        self.db.tieba_akg.insert(dict(item))
