# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exporters import CsvItemExporter
from scrapy import signals
from datetime import datetime
from scrapy_redis.pipelines import RedisPipeline


class StreetcheckPipeline(RedisPipeline):

    # @classmethod
    # def from_crawler(cls, crawler):
    #     pipeline = cls()
    #     crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
    #     crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
    #     return pipeline

    # def spider_opened(self, spider):
    #     self.file = open('streets.csv', 'w+b')
    #     self.exporter = CsvItemExporter(self.file)
    #     self.exporter.start_exporting()

    # def spider_closed(self, spider):
    #     self.exporter.finish_exporting()
    #     self.file.close()

    def process_item(self, item, spider):
        item['crawled'] = datetime.utcnow()
        item['spider'] = spider.name
        return super().process_item(item, spider)


