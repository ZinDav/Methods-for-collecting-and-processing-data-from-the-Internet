from lxml import html
import requests
from pymongo import MongoClient
from pprint import pprint

# Написать приложение, которое собирает основные новости с сайта lenta.ru.
# Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
# Сложить собранные новости в БД

url = 'https://lenta.ru'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)\
                            Chrome/97.0.4692.99 Safari/537.36'}
response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)
news_item = dom.xpath("//div[@class='topnews__column']//a")

client = MongoClient('127.0.0.1', 27017)
db = client['news']
lenta = db.lenta

for n in news_item:
    news = dict()
    source = 'lenta.ru'
    name = n.xpath(".//text()")[0]
    link = f'{url}{n.xpath("./@href")[0]}'
    date = n.xpath(".//text()")[1]
    uid = n.xpath("./@href")[0]
    news['_id'] = uid
    news['source'] = source
    news['name'] = name
    news['link'] = link
    news['date'] = date
    lenta.insert_one(news)

for el in lenta.find({}):
    pprint(el)
