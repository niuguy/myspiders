# -*- coding: utf-8 -*-
import scrapy
import pickle
import time
from scrapy.loader import ItemLoader
from etsy.items import Shop

class ShopsSpider(scrapy.Spider):
    name = 'shops'


    def start_requests(self):
        shop_lists = pickle.load(open('open_bra_shop_lists.pkl', 'rb'))
        print('------->',len(shop_lists))
        for shop in shop_lists:
            url = 'https://www.etsy.com/uk/shop/' + shop
            time.sleep(1)
            yield scrapy.Request(url = url, callback=self.parse)


    def parse(self, response):
        # s = ItemLoader(item=Shop(), response = response)
        name = response.xpath('//h1[@class="mb-xs-1"]/text()').extract()
        sales_1 = response.xpath('//span[@class="mr-xs-2 pr-xs-2 br-xs-1"]/a/text()').re(r"\d+")
        sales_2 = response.xpath('//span[@class="mr-xs-2 pr-xs-2 br-xs-1"]/text()').re(r"\d+")
        sales = sales_1 or sales_2
        location = response.xpath('//span[@class="shop-location mr-xs-2 pr-xs-2 br-xs-1"]/text()').extract()
        since = response.xpath('//span[@class="etsy-since no-wrap"]/text()').re(r"\d+")
        url = 'https://www.etsy.com/uk/shop/' + name[0]

        yield{
            'name': name,   
            'location': location,
            'sales': sales,
            'since': since,
            'url' : url
        }
        # s.add_xpath('name','//h1[@class="mb-xs-1"]/text()')

        # return s.load_item()

