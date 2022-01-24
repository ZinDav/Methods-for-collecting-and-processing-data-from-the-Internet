import requests
import json

user = 'ZinDav'
url = f'https://api.github.com/users/{user}/repos'

res = requests.get(url).json()
repos = list()
for i in range(len(res)):
    repos.append(res[i]['name'])
print(f'Список репозиториев пользователя {user}: {repos}')
with open('repos.json', 'w') as js_f:
    json.dump(res, js_f)