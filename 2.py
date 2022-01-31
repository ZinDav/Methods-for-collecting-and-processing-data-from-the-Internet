# Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой
# больше введённой суммы (необходимо анализировать оба поля зарплаты).
# То есть цифра вводится одна, а запрос проверяет оба поля

from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['HH']
vacancies = db.vacancies

salary = 100000
for vacancy in vacancies.find({'$or': [{'Min_salary': {'$gt': salary}},
                                       {'Max_salary': {'$gt': salary}}],
                               'Currency': 'руб.'}):
    pprint(vacancy)
