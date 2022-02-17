# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst

class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    type = scrapy.Field()
    main_user = scrapy.Field()
    main_user_id = scrapy.Field()
    user_id = scrapy.Field()
    username = scrapy.Field()
    full_name = scrapy.Field()
    photo = scrapy.Field()
    is_private = scrapy.Field()
    _id = scrapy.Field()
