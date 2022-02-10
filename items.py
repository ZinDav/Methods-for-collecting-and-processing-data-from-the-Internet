# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    main_price = scrapy.Field()
    sail_price = scrapy.Field()
    cur = scrapy.Field()
    rating = scrapy.Field()
    _id = scrapy.Field()
