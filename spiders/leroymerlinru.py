import scrapy
from scrapy.http import HtmlResponse
from goodparser.items import GoodparserItem
from scrapy.loader import ItemLoader

# 1) Взять любую категорию товаров на сайте Леруа Мерлен. Собрать следующие данные:
# название;
# все фото;
# ссылка;
# цена.
# Реализуйте очистку и преобразование данных с помощью ItemLoader. Цены должны быть в виде числового значения.
#
# Дополнительно:
# 2)Написать универсальный обработчик характеристик товаров, который будет формировать данные
# вне зависимости от их типа и количества.
# 3)Реализовать хранение скачиваемых файлов в отдельных папках, каждая из которых должна соответствовать
# собираемому товару.

class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={kwargs.get("search")}']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[@data-qa="product-name"]')
        for link in links:
            yield response.follow(link, callback=self.good_parse)
        next_page = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()
        while next_page:
            yield response.follow(next_page, callback=self.parse)

    def good_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=GoodparserItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_value('link', response.url)
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_xpath('photos', '//source[@media=" only screen and (min-width: 1024px)"]/@srcset')
        loader.add_xpath('ch_key', '//dt/text()')
        loader.add_xpath('ch_value', '//dd/text()')
        yield loader.load_item()
