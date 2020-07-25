# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class Street(Item):
    crawled = Field()
    spider = Field()
    street_code = Field()
    cn_count = Field()
    cn_rate = Field()
    ab_people_rate = Field()
    white_rate = Field()
    fulltime_rate = Field()
