# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StreetcheckItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Street(scrapy.Item):
    street_code = scrapy.Field()
    cn_count = scrapy.Field()
    cn_rate = scrapy.Field()
    ab_people_rate = scrapy.Field()
    white_rate = scrapy.Field()
    fulltime_rate = scrapy.Field()
