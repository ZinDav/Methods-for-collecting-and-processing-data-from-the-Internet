from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
from pymongo import errors

# Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# которая будет добавлять только новые вакансии в вашу базу.

client = MongoClient('127.0.0.1', 27017)
db = client['HH']
vacancies = db.vacancies


class ParseHHVacancies:
    url = 'https://hh.ru/search/vacancy'

    def find_vacancies(self, search, collection):
        params = {
            'area': 113,
            'text': search,
            'hhtmFrom': 'vacancy_search_list'
        }
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
                    (KHTML, like Gecko)Chrome/97.0.4692.99 Safari/537.36'}
        response = requests.get(self.url, params=params, headers=headers)
        dom = BeautifulSoup(response.text, 'html.parser')
        max_page = int(dom.find_all('span', {'class': 'pager-item-not-in-short-range'})[-1].find('a').getText())
        for i in range(max_page):
            page = i
            params = {
                'area': 113,
                'text': search,
                'page': page,
                'hhtmFrom': 'vacancy_search_list'
            }
            response = requests.get(self.url, params=params, headers=headers)
            dom = BeautifulSoup(response.text, 'html.parser')
            main = dom.find_all('span', {'data-qa': "bloko-header-3", 'class': "bloko-header-section-3"})
            for part in main:
                vac_dict = dict()
                vac_dict['_id'] = part.find('a').get('href').split('/')[-1].split('?')[0]
                vac_dict['Link'] = part.find('a').get('href')
                vac_dict['Source'] = 'hh.ru'
                vac_dict['Vacancy_name'] = part.find('a').text
                try:
                    salary = part.parent.next_sibling.text.replace('\u202f', '')
                    split_sal = salary.split()
                    if split_sal[0] == 'от':
                        vac_dict['Min_salary'] = int(split_sal[1])
                        vac_dict['Max_salary'] = None
                        vac_dict['Currency'] = split_sal[-1]
                    elif split_sal[0] == 'до':
                        vac_dict['Min_salary'] = None
                        vac_dict['Max_salary'] = int(split_sal[1])
                        vac_dict['Currency'] = split_sal[-1]
                    else:
                        vac_dict['Min_salary'] = int(split_sal[0])
                        vac_dict['Max_salary'] = int(split_sal[2])
                        vac_dict['Currency'] = split_sal[-1]
                except AttributeError:
                    vac_dict['Min_salary'] = None
                    vac_dict['Max_salary'] = None
                    vac_dict['Currency'] = None
                except IndexError:
                    vac_dict['Min_salary'] = None
                    vac_dict['Max_salary'] = None
                    vac_dict['Currency'] = None
                try:
                    collection.insert_one(vac_dict)
                    print('Vacancy is added')
                except errors.DuplicateKeyError:
                    print('Vacancy already exists')
        return collection


s = input('Input vacancy name: ')

phhv = ParseHHVacancies()
vacancies = phhv.find_vacancies(s, vacancies)
