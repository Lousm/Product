# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductclassificationItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    oneclassname = scrapy.Field()
    twoclassname = scrapy.Field()
    threeclassname = scrapy.Field()
    fourclassname = scrapy.Field()
    fiveclassname = scrapy.Field()

    pass
