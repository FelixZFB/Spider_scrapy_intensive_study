# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import scrapy
from scrapy.exceptions import DropItem

class TiebaPipeline(object):
    # def process_item(self, item, spider):
    #     return item

    def __init__(self):
        self.file = open('papers.json', 'w', encoding='utf-8')

    # 将ITEM里面的信息写入到一个json文件中
    def process_item(self, item, spider):
        # 判断item字典对象中title对应的是否还有值
        if item['title']:
            # 将item字典类型的数据转换成json格式的字符串,
            # 注意json.dumps序列化时对中文默认使用的ascii编码，要想写入中文，加上ensure_ascii=False
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file.write(line)
            return item
        else:
            raise DropItem("Missing title in %s" % item)
