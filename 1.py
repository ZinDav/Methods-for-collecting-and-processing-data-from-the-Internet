from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
from pprint import pprint

# Написать программу, которая собирает товары «В тренде» с сайта техники mvideo и складывает данные в БД.

client = MongoClient('127.0.0.1', 27017)
db = client['shop']
pr = db.pr

chrome_options = Options()
chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
driver.get('https://www.mvideo.ru/')

part = 1
while part < 6:
    try:
        elem = driver.find_element(By.XPATH, '//span[contains(text(), "В тренде")]')
        break
    except NoSuchElementException:
        driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight / 5 * {part});")
        driver.implicitly_wait(10)
    part += 1

elem = driver.find_element(By.XPATH, '//span[contains(text(), "В тренде")]')
elem.click()

elem = driver.find_elements(By.CLASS_NAME, 'mvid-carousel-inner')[5]
goods = elem.find_elements(By.CLASS_NAME, 'product-mini-card__name')

for good in goods:
    good_dict = dict()
    name = good.text
    uid = good.find_element(By.XPATH, './/a').get_attribute('href').split('-')[-1]
    link = good.find_element(By.XPATH, './/a').get_attribute('href')
    price = elem.find_elements(By.CLASS_NAME, 'product-mini-card__price')[goods.index(good)].text
    price = int(price.split('\n')[0].replace(' ', ''))
    good_dict['_id'] = uid
    good_dict['name'] = name
    good_dict['link'] = link
    good_dict['price'] = price
    pr.insert_one(good_dict)

for el in pr.find({}):
    pprint(el)
