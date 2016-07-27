# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MojiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ImageItem(scrapy.Item):
    pid = scrapy.Field()
    country = scrapy.Field()
    province = scrapy.Field()
    disrict = scrapy.Field()
    location = scrapy.Field()
    lon = scrapy.Field()
    lat = scrapy.Field()
    ptime = scrapy.Field()
    pname = scrapy.Field()