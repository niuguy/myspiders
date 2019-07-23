# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import redis


class EtsyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    
    pass

class Shop(scrapy.Item):
    search_key = scrapy.Field()
    shop_name = scrapy.Field()
    search_pages = scrapy.Field()
    sales = scrapy.Field()
    location = scrapy.Field()
    since = scrapy.Field()
    url = scrapy.Field()
    comment_counts = scrapy.Field()
    comment_value = scrapy.Field()
    record_time = scrapy.Field()
    record_date = scrapy.Field()


class Listing(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    # delivery = scrapy.Field()
    # freight = scrapy.Field()
    shop_name = scrapy.Field()
    # shop_sails = scrapy.Field()
    # description = scrapy.Field()
    # tags = scrapy.Field()

    