# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EtsyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    
    pass

class Shop(scrapy.Item):
    name = scrapy.Field()
    sales = scrapy.Field()
    location = scrapy.Field()
    since = scrapy.Field()
    url = scrapy.Field()

