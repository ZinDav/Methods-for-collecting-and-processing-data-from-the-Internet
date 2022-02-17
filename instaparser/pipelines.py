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


class InstaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.followers

    def process_item(self, item, spider):
        item['_id'] = f'{item["main_user_id"]}_{item["user_id"]}'
        follower = self.mongobase[spider.name]
        following = self.mongobase[spider.name]
        if item['type'] == 'followers':
            try:
                follower.insert_one(item)
            except DuplicateKeyError:
                pass
            return item
        else:
            try:
                following.insert_one(item)
            except DuplicateKeyError:
                pass
            return item

    def find_item(self, uid):
        follower = self.mongobase['instagramcom']
        following = self.mongobase['instagramcom']
        for f in follower.find({'main_user_id': uid}):
            pprint(f)
        for f in following.find({'main_user_id': uid}):
            pprint(f)