# -*- coding: utf-8 -*-
import scrapy
import pickle
import time
from scrapy.loader import ItemLoader
from etsy.items import Shop
from scrapy.exporters import CsvItemExporter
import datetime

class ShopsSpider(scrapy.Spider):
    name = 'shops'

    def __init__(self, kw='', pn=10 , **kwargs):
        self.shop_lists = set()
        self.key_word = kw
        self.page_num = pn
        file_name = 'results/{0}_top{1}pages_shops_{2}.csv'.format(self.key_word.replace(" ","-"), self.page_num, datetime.datetime.now().strftime("%y%m%d"))
        self.file = open(file_name, 'w+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()
        
    
    def start_requests(self):
        for i in range(self.page_num):
            url = 'https://www.etsy.com/uk/search?q='+self.key_word+'&ref=pagination&page='+ str(i)
            time.sleep(1)
            yield scrapy.Request(url = url, callback=self.parse_info)


    def parse_info(self, response):
        shop_list = response.xpath('//p[@class="text-gray-lighter text-body-smaller display-inline-block"]/text()').extract()
        for shop in shop_list:
            if shop in self.shop_lists:
                continue
            self.shop_lists.add(shop)
            shop_url =  'https://www.etsy.com/uk/shop/' + shop
            yield scrapy.Request(url = shop_url, callback=self.parse_detail)



    def parse_detail(self, response):
        # s = ItemLoader(item=Shop(), response = response)
        shop = Shop()
        shop['name'] = response.xpath('//h1[@class="mb-xs-1"]/text()').extract()
        shop['url'] = 'https://www.etsy.com/uk/shop/' + shop['name'][0]
        sales_1 = response.xpath('//span[@class="mr-xs-2 pr-xs-2 br-xs-1"]/a/text()').re(r"\d+")
        sales_2 = response.xpath('//span[@class="mr-xs-2 pr-xs-2 br-xs-1"]/text()').re(r"\d+")
        sales = sales_1 or sales_2
        shop['sales'] = sales
        comment_counts = response.xpath('//span[@class="total-rating-count text-gray-lighter ml-xs-1"]/text()').re(r"\d+")
        shop['comment_counts'] =  comment_counts
        comment_value = response.xpath('//input[@name="rating"]/@value')[0].extract()
        shop['comment_value'] = comment_value
        location = response.xpath('//span[@class="shop-location mr-xs-2 pr-xs-2 br-xs-1"]/text()').extract()
        shop['location'] = location
        since = response.xpath('//span[@class="etsy-since no-wrap"]/text()').re(r"\d+")
        shop['since'] = since
        self.exporter.export_item(shop)

        return shop
        
    def closed(self, reason):
        self.exporter.finish_exporting()
        self.file.close()

