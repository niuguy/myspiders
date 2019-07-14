# -*- coding: utf-8 -*-
import scrapy
import time
import pickle


class ShopdetailrSpider(scrapy.Spider):
    name = 'shopdetail'
    
    def __init__(self):
        self.shop_lists = set()
        self.key_word = 'open bra'
        self.page_num = 10


    def start_requests(self):
        for i in range(self.page_num):
            url = 'https://www.etsy.com/uk/search?q='+self.key_word+'&ref=pagination&page='+ str(i)
            time.sleep(1)
            yield scrapy.Request(url = url, callback=self.parse)

    def parse(self, response):
        shop_list = response.xpath('//p[@class="text-gray-lighter text-body-smaller display-inline-block"]/text()').extract()
        self.shop_lists.update(shop_list)
        
    
    def closed(self, reason):
        pickle.dump(self.shop_lists,open('open_bra_shop_lists.pkl','wb'))
        print('well done')


        
