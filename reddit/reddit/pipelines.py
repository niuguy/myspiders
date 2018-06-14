# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import CsvItemExporter

class RedditPipeline(object):
    def process_item(self, item, spider):
        return item

class CsvPipeline(object):

	def open_spider(self, spider):
		fields_to_export = {'title'}
		dest_file_path = 'data/{}_posts.csv'.format(spider.name)
		dest_file = open(dest_file_path, 'w+')
		self.exporter = CsvItemExporter(dest_file)
		self.exporter.fields_to_export = fields_to_export
		self.exporter.start_exporting()

	def close_spider(self, spider):
		self.exporter.finish_exporting()


	def process_item(self, item, spider):

		self.exporter.export_item(item)
		return item 



