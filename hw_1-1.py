'''
Посмотреть документацию к API GitHub,
разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json;
написать функцию, возвращающую список репозиториев.
'''

import json
import requests
from pprint import pprint


def get_response(user):
    url = f"https://api.github.com/users/{user}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        return response
    return None


def save_json(response_get):
    with open("repos_list.json", "w") as f:
        json.dump(response_get.json(), f)


def repos_list(response_join):
    user_list = []
    for i in response_join.json():
        user_list.append(i["name"])
    return user_list


username = "SergChupin"

res = get_response(username)
save_json(res)
repos_lists = repos_list(res)

pprint(repos_lists)
