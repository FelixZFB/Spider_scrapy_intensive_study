# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TiebaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    task_id = scrapy.Field()

    tieba_name = scrapy.Field()
    title = scrapy.Field()
    href = scrapy.Field()
    author = scrapy.Field()
    reply_num = scrapy.Field()



