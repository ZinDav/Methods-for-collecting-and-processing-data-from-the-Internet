# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def process_price(price):
    clean_price = price.replace(' ', '')
    try:
        clean_price = int(clean_price)
        return clean_price
    except:
        return clean_price


def process_char(val):
    return val.replace('\n            ', '').replace('    ', '')


class GoodparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(process_price), output_processor=TakeFirst())
    ch_key = scrapy.Field()
    ch_value = scrapy.Field(input_processor=MapCompose(process_char))
    characteristics = scrapy.Field()
    _id = scrapy.Field()
