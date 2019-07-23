# -*- coding: utf-8 -*-
import scrapy
import pickle
import time
from scrapy.loader import ItemLoader
from etsy.items import Listing
from scrapy.exporters import CsvItemExporter
from scrapy.exporters import JsonItemExporter
import datetime
import redis

class ListingsSpider(scrapy.Spider):
    name = 'listings'

    def __init__(self, kw='', pn=10 , **kwargs):
        self.shop_lists = set()
        self.key_word = kw
        self.page_num = int(pn)
        file_name = 'results/listings/top{0}pages_listings_{1}.json'.format(self.page_num, datetime.datetime.now().strftime("%y%m%d"))
        self.file = open(file_name, 'w+b')
        self.exporter = JsonItemExporter(self.file)
        self.exporter.start_exporting()
        
    
    def start_requests(self):
        for i in range(self.page_num):
            url_best = 'https://www.etsy.com/uk/market/best_selling_items?page='+str(i)
            time.sleep(1)
            yield scrapy.Request(url = url_best, callback=self.parse_info)


    def parse_info(self, response):
        listing_urls = response.xpath('//div[@data-behat-listing-card]/a/@href').extract()
        for url in listing_urls:

            yield scrapy.Request(url = url, callback=self.parse_detail)



    def parse_detail(self, response):
        # s = ItemLoader(item=Shop(), response = response)
        listing = Listing()
        listing['title'] = response.xpath('//h2[@class="text-gray text-truncate mb-xs-0 text-body"]/text()').get()
        listing['price'] = response.xpath('//span[@class="text-largest strong override-listing-price"]/text()').re(r'(\d+\.\d{1,2})')[0]
        listing['shop_name'] = response.xpath('//a[@class="text-link-no-underline text-gray-lightest"]/text()').get()
        # tags = response.xpath('//a[@class="btn btn-secondary"]/text()').extract()
        # listing['tags'] = '-'.join(tags)
        # listing['description'] = response.xpath('//div[@class=" text-gray prose  mb-xs-0"]/div/text()').extract()
       
        self.exporter.export_item(listing)

        return listing
        
    def closed(self, reason):
        self.exporter.finish_exporting()
        self.file.close()
