from lxml import html
import requests
from pymongo import MongoClient
from pprint import pprint

# Написать приложение, которое собирает основные новости с сайта yandex.ru/news.
# Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
# Сложить собранные новости в БД

url = 'https://yandex.ru/news'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)\
                            Chrome/97.0.4692.99 Safari/537.36'}
response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)
news_item = dom.xpath('//section[@aria-labelledby="Экономика4"]//div[contains(@class, "mg-grid__item")]')

client = MongoClient('127.0.0.1', 27017)
db = client['news']
yandex = db.yandex

for n in news_item:
    news = dict()
    source = 'yandex.ru/news'
    name = n.xpath(".//a[@class='mg-card__link']/text()")[0].replace('\xa0', ' ')
    link = n.xpath(".//a[@class='mg-card__link']/@href")[0]
    date = n.xpath(".//span[@class='mg-card-source__time']/text()")[0]
    uid = n.xpath(".//a[@class='mg-card__link']/@href")[0].split('=')[-1]
    news['_id'] = uid
    news['source'] = source
    news['name'] = name
    news['link'] = link
    news['date'] = date
    yandex.insert_one(news)

for el in yandex.find({}):
    pprint(el)
