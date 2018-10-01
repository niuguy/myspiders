# -*- coding: utf-8 -*-
import scrapy
import time

class BringfidoSpider(scrapy.Spider):
    name = 'bringfido'
    # allowed_domains = ['https://www.bringfido.com/travel/airline_policies/']
    start_urls = ['https://www.bringfido.com/travel/airline_policies/']

    def parse(self, response):
    	# subpage of airline policy introduction
    	hrefs = response.xpath('//a[@class="anchor"]/@href').extract()
    	for href in hrefs:  
    		yield response.follow(href, self.parse_airline_url)

    def parse_airline_url(self, response):
    	airline_name = response.xpath('//h1[@itemprop="name"]/text()').extract()
    	airline_url = response.xpath('//a[@class="big-property-button"]/@href').extract()
    	yield {
    		'url': airline_url,
    		'airline':  airline_name,
    	}

