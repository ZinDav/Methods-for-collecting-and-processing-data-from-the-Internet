from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы
# получаем должность) с сайтов HH(обязательно) и/или Superjob(по желанию). Приложение должно
# анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия (можно указать статично для hh - hh.ru, для superjob - superjob.ru)

search = input('Input vacancy name: ')
url = 'https://hh.ru/search/vacancy'
page = 0
params = {
        'area': 113,
        'text': search,
        'page': page,
        'hhtmFrom': 'vacancy_search_list'
}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
            Chrome/97.0.4692.99 Safari/537.36'}

response = requests.get(url, params=params, headers=headers)
dom = BeautifulSoup(response.text, 'html.parser')


max_page = int(dom.find_all('span', {'class': 'pager-item-not-in-short-range'})[-1].find('a').getText())
name = list()
min_sal = list()
max_sal = list()
currency = list()
link = list()
web = list()

for i in range(max_page):
    page = i
    response = requests.get(url, params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    main = dom.find_all('span', {'data-qa': "bloko-header-3", 'class': "bloko-header-section-3"})
    for part in main:
        name.append(part.find('a').text)
        link.append(part.find('a').get('href'))
        web.append('hh.ru')
        try:
            salary = part.parent.next_sibling.text.replace('\u202f', '')
            split_sal = salary.split()
            if split_sal[0] == 'от':
                min_sal.append(split_sal[1])
                max_sal.append(None)
                currency.append(split_sal[-1])
            elif split_sal[0] == 'до':
                min_sal.append(None)
                max_sal.append(split_sal[1])
                currency.append(split_sal[-1])
            else:
                min_sal.append(split_sal[0])
                max_sal.append(split_sal[2])
                currency.append(split_sal[-1])
        except AttributeError:
            min_sal.append(None)
            max_sal.append(None)
            currency.append(None)
        except IndexError:
            min_sal.append(None)
            max_sal.append(None)
            currency.append(None)

research = {
    'Vacancy_name': name,
    'Min_salary': min_sal,
    'Max_salary': max_sal,
    'Currency': currency,
    'Link': link,
    'Source': web
}
with open('vacancy.json', 'w', encoding='utf8') as file:
    json.dump(research, file, ensure_ascii=False)

research = pd.DataFrame(research)
print(research)
