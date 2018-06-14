# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector

from ..items import PostItem


class TravelSpider(scrapy.Spider):
    name = 'travel'
    allowed_domains = ['www.reddit.com/r/travel/']
    start_urls = ['http://www.reddit.com/r/travel']

    def parse(self, response):
    	titles = response.xpath('//h2/text()').extract()

    	for title in titles:
    		yield PostItem(title=title)

    	
        
