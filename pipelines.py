# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class BookparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.books

    def process_item(self, item, spider):
        item['_id'] = item['link'].split('/')[-2].split('-')[-1]
        item['sail_price'], item['cur'] = self.process_price(item['sail_price'])
        item['main_price'], item['cur'] = self.process_price(item['main_price'])
        item['rating'] = item['rating'].split()[0]
        book = self.mongobase[spider.name]
        try:
            book.insert_one(item)
        except DuplicateKeyError:
            pass
        return item

    @staticmethod
    def process_price(price):
        if price is not None:
            p, c = price.replace('\xa0', '').split()
            return int(p), c
        else:
            return None, None
