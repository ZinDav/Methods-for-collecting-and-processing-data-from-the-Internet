import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem

# 1) Создать пауков по сбору данных о книгах с сайта book24.ru
# 2) Каждый паук должен собирать:
# * Ссылку на книгу
# * Наименование книги
# * Автор(ы)
# * Основную цену
# * Цену со скидкой
# * Рейтинг книги
# 3) Собранная информация должна складываться в базу данных


class Book24ruSpider(scrapy.Spider):
    page = 1
    name = 'book24ru'
    allowed_domains = ['book24.ru']
    start_urls = [f'https://book24.ru/search/page-{page}/?q=программирование']

    def parse(self, response: HtmlResponse):
        if response.status != 404:
            links = response.xpath("//div[contains(@class, 'catalog__product-list-holder')]//\
                                            a[contains(@class, 'product-card__name')]/@href").getall()
            for link in links:
                yield response.follow(link, callback=self.book_parse)
            self.page += 1
            next_page = f'https://book24.ru/search/page-{self.page}/?q=программирование'
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        link = response.url
        name = response.xpath('//h1/text()').get().replace('\n', '')
        author = response.xpath("//div[contains(@class, 'product-characteristic__value')]//text()").get()
        if response.xpath("//span[contains(@class, 'product-sidebar-price__price-old')]\
                                                                /text()").get() is not None:
            main_price = response.xpath("//span[contains(@class, 'product-sidebar-price__price-old')]\
                                                                            /text()")[0].get()
            sail_price = response.xpath("//span[contains(@class, 'product-sidebar-price__price')]\
                                                                            /text()")[1].get()
        else:
            main_price = response.xpath("//span[contains(@class, 'product-sidebar-price__price')]\
                                                                            /text()").get()
            sail_price = None
        rating = response.xpath("//span[@class='rating-widget__main-text']/text()").get()
        yield BookparserItem(link=link, name=name, author=author, main_price=main_price,
                             sail_price=sail_price, rating=rating)
