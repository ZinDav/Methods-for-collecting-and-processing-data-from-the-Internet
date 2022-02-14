# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class GoodparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.goods

    def process_item(self, item, spider):
        item['characteristics'] = dict(zip(item['ch_key'], item['ch_value']))
        del item['ch_key']
        del item['ch_value']
        item['_id'] = item['link'].split('/')[-2].split('-')[-1]
        good = self.mongobase[spider.name]
        try:
            good.insert_one(item)
        except DuplicateKeyError:
            pass
        return item


class GoodImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        uid = item['link'].split('/')[-2].split('-')[-1]
        return f"{uid} {item['name']}/{item['photos'].index(request.url)}.jpg"
